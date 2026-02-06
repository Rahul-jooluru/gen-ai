import json
import os
import re
from flask import Blueprint, request, jsonify
from datetime import datetime
from ai.llm_client import ask_llm

chat_bp = Blueprint("chat", __name__)

DATA_FILE = "data/photos.json"
CONTACTS_FILE = "data/contacts.json"
SHARES_FILE = "data/shares.json"


def load_photos():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_photos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def load_shares():
    try:
        with open(SHARES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_shares(data):
    with open(SHARES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def normalize_tags(tags):
    if not tags:
        return []
    if isinstance(tags, list):
        return [t.lower() for t in tags]
    return []


def extract_keywords(text):
    """Enhanced keyword extraction for better search"""
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "is", "are", "was", "were", "be", "been", "being", "have", "has",
        "had", "do", "does", "did", "will", "would", "could", "should", "may",
        "might", "must", "can", "i", "you", "he", "she", "it", "we", "they",
        "me", "him", "her", "us", "them", "my", "your", "his", "its", "our",
        "pics", "pictures", "photos", "photo", "image", "images", "delete"
    }
    
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    keywords = [
        word.strip() 
        for word in text.split() 
        if len(word.strip()) > 2 and word.strip() not in stop_words
    ]
    return list(set(keywords))


def match_photos(keywords, photos):
    """Smart matching algorithm"""
    results = []
    
    for photo in photos:
        tags = normalize_tags(photo.get("tags", []))
        match_score = 0
        
        for keyword in keywords:
            for tag in tags:
                if keyword == tag:
                    match_score += 3
                elif keyword in tag or tag in keyword:
                    match_score += 1
        
        if match_score > 0:
            result = photo.copy()
            result['match_score'] = match_score
            results.append(result)
    
    results.sort(key=lambda x: x['match_score'], reverse=True)
    
    for r in results:
        del r['match_score']
    
    return results


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({
            "message": "Ask me something about your photos - what would you like to find?",
            "photos": []
        })

    photos = load_photos()

    # Check command type
    is_delete_command = any(word in query.lower() for word in ["delete", "remove", "erase", "discard"])
    is_share_command = any(word in query.lower() for word in ["share", "send", "forward"])
    
    # Extract keywords (tries LLM first, falls back to smart extraction)
    try:
        keywords_text = ask_llm(
            f"Extract important visual keywords from: {query}"
        )
        keywords = [
            k.strip().lower()
            for k in keywords_text.replace(",", " ").split()
            if len(k.strip()) > 2
        ]
        print(f"✅ LLM Keywords: {keywords}")
    except Exception as e:
        print(f"⚠️  LLM failed, using smart extraction: {e}")
        keywords = extract_keywords(query)
        print(f"✅ Extracted Keywords: {keywords}")

    # Match photos with smart algorithm
    results = match_photos(keywords, photos)

    # Handle delete command
    if is_delete_command and results:
        deleted_count = len(results)
        deleted_ids = [photo['id'] for photo in results]
        
        # Remove from photos.json
        updated_photos = [p for p in photos if p['id'] not in deleted_ids]
        save_photos(updated_photos)
        
        # Delete image files
        for photo in results:
            filename = photo.get("url", "").split("/")[-1]
            file_path = os.path.join("storage/images", filename)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"   🗑️  Deleted: {filename}")
            except Exception as e:
                print(f"   ⚠️  Failed to delete file {filename}: {e}")
        
        message = f"🗑️  Deleted {deleted_count} photo(s) matching '{query}'!"
        print(f"🗑️  DELETE: '{query}' → Deleted {deleted_count} photos")
        
        return jsonify({
            "message": message,
            "photos": results
        })
    
    # Handle share command
    if is_share_command and results:
        # Extract contact name from query
        query_lower = query.lower()
        contact_name = None
        
        # Try to find contact name in query
        contacts = load_contacts()
        for contact in contacts:
            if contact["name"].lower() in query_lower:
                contact_name = contact["name"]
                break
        
        if not contact_name:
            message = f"📱 Found {len(results)} photo(s) to share, but which contact? Try: 'share to [contact_name]'"
            return jsonify({
                "message": message,
                "photos": results
            })
        
        # Create share record
        share_record = {
            "id": f"{contact_name.lower().replace(' ', '_')}_{len(load_shares())}",
            "contact_name": contact_name,
            "photo_ids": [p['id'] for p in results],
            "photo_count": len(results),
            "shared_at": datetime.utcnow().isoformat()
        }
        
        shares = load_shares()
        shares.append(share_record)
        save_shares(shares)
        
        message = f"✅ Shared {len(results)} photo(s) with {contact_name}! 📱"
        print(f"📤 SHARE: '{query}' → Shared {len(results)} photos to {contact_name}")
        
        return jsonify({
            "message": message,
            "photos": results
        })
    
    # Regular search (not delete or share)
    if results:
        message = f"🎉 Found {len(results)} photo(s) matching '{query}'!"
    else:
        message = f"Hmm, couldn't find photos matching '{query}'. Try different words like color, objects, or settings."

    print(f"📸 Query: '{query}' → Keywords: {keywords} → Found: {len(results)} photos")

    return jsonify({
        "message": message,
        "photos": results
    })

