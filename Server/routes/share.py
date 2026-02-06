import json
import os
import urllib.parse
from flask import Blueprint, request, jsonify
from datetime import datetime

share_bp = Blueprint("share", __name__)

CONTACTS_FILE = "data/contacts.json"
SHARES_FILE = "data/shares.json"
DATA_FILE = "data/photos.json"
USER_PROFILE_FILE = "data/user_profile.json"


def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_contacts(data):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_shares():
    try:
        with open(SHARES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_shares(data):
    with open(SHARES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_photos():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def load_user_profile():
    """Load user profile (your name/identity)"""
    try:
        with open(USER_PROFILE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"name": "You", "created_at": datetime.utcnow().isoformat()}


def save_user_profile(data):
    """Save user profile"""
    os.makedirs("data", exist_ok=True)
    with open(USER_PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ==================== USER PROFILE ====================

@share_bp.route("/user/profile", methods=["GET"])
def get_user_profile():
    """Get your user profile"""
    return jsonify(load_user_profile())


@share_bp.route("/user/profile", methods=["POST"])
def set_user_profile():
    """Set your name/identity"""
    data = request.get_json() or {}
    name = data.get("name", "You").strip()
    
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    profile = {
        "name": name,
        "created_at": datetime.utcnow().isoformat()
    }
    
    save_user_profile(profile)
    return jsonify(profile), 200


# ==================== CONTACTS ====================

@share_bp.route("/contacts", methods=["GET"])
def get_contacts():
    """Get all contacts"""
    return jsonify(load_contacts())


@share_bp.route("/contacts", methods=["POST"])
def add_contact():
    """Add a new contact"""
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    contacts = load_contacts()
    
    # Check if contact already exists
    if any(c["name"].lower() == name.lower() for c in contacts):
        return jsonify({"error": "Contact already exists"}), 400
    
    contact = {
        "id": name.lower().replace(" ", "_"),
        "name": name,
        "phone": phone,
        "added_at": datetime.utcnow().isoformat()
    }
    
    contacts.append(contact)
    save_contacts(contacts)
    
    return jsonify(contact), 201


@share_bp.route("/contacts/<contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    """Delete a contact"""
    contacts = load_contacts()
    remaining = [c for c in contacts if c["id"] != contact_id]
    
    if len(remaining) == len(contacts):
        return jsonify({"error": "Contact not found"}), 404
    
    save_contacts(remaining)
    return jsonify({"status": "deleted"}), 200


# ==================== SHARING ====================

@share_bp.route("/share", methods=["POST"])
def share_photos():
    """Share photos with a contact - creates both send & receive records + WhatsApp link"""
    data = request.get_json() or {}
    photo_ids = data.get("photo_ids", [])
    contact_name = data.get("contact_name", "").strip()
    
    if not photo_ids or not contact_name:
        return jsonify({"error": "photo_ids and contact_name are required"}), 400
    
    user_profile = load_user_profile()
    contacts = load_contacts()
    contact = next((c for c in contacts if c["name"].lower() == contact_name.lower()), None)
    
    if not contact:
        return jsonify({"error": f"Contact '{contact_name}' not found"}), 404
    
    photos = load_photos()
    shared_photos = [p for p in photos if p["id"] in photo_ids]
    
    if not shared_photos:
        return jsonify({"error": "No photos found"}), 404
    
    shares = load_shares()
    
    # CREATE OUTGOING SHARE RECORD
    share_record = {
        "id": f"{contact['id']}_{len(shares)}",
        "type": "sent",
        "from": user_profile.get("name", "You"),
        "to": contact["name"],
        "to_phone": contact.get("phone"),
        "photo_ids": photo_ids,
        "photo_count": len(shared_photos),
        "shared_at": datetime.utcnow().isoformat(),
        "status": "delivered"
    }
    
    # CREATE CORRESPONDING RECEIVE RECORD FOR RECIPIENT
    receive_record = {
        "id": f"recv_{contact['id']}_{len(shares)}",
        "type": "received",
        "from": user_profile.get("name", "You"),
        "to": contact["name"],
        "photo_ids": photo_ids,
        "photo_count": len(shared_photos),
        "shared_at": datetime.utcnow().isoformat(),
        "status": "unread"
    }
    
    shares.append(share_record)
    shares.append(receive_record)
    save_shares(shares)
    
    # GENERATE WHATSAPP MESSAGE
    photo_tags = ", ".join(set(tag for photo in shared_photos for tag in photo.get("tags", [])[:3]))
    whatsapp_message = f"📸 {user_profile.get('name', 'I')} shared {len(shared_photos)} photo(s) with you!"
    if photo_tags:
        whatsapp_message += f"\n🏷️ Tags: {photo_tags}"
    whatsapp_message += f"\n⏰ {datetime.utcnow().strftime('%B %d, %Y')}"
    
    # WhatsApp API link (works on web and mobile)
    phone = contact.get("phone", "").replace(" ", "").replace("-", "")
    if phone and not phone.startswith("+"):
        phone = f"+91{phone}" if len(phone) == 10 else f"+{phone}"
    
    whatsapp_link = f"https://wa.me/{phone.replace('+', '')}?text={urllib.parse.quote(whatsapp_message)}"
    
    print(f"   ✅ SHARED: {user_profile.get('name')} → {contact['name']} ({len(shared_photos)} photo(s))")
    print(f"   📱 WhatsApp: {whatsapp_link}")
    
    return jsonify({
        "message": f"✅ Shared {len(shared_photos)} photo(s) with {contact['name']}!",
        "share_record": share_record,
        "receive_record": receive_record,
        "whatsapp_link": whatsapp_link,
        "whatsapp_message": whatsapp_message
    }), 201


@share_bp.route("/shares", methods=["GET"])
def get_shares():
    """Get all share history (both sent and received)"""
    return jsonify(load_shares())


@share_bp.route("/shares/sent", methods=["GET"])
def get_sent_shares():
    """Get all photos I've shared with others"""
    shares = load_shares()
    photos = load_photos()
    
    sent = [s for s in shares if s.get("type") == "sent"]
    
    for share in sent:
        share["photos"] = [p for p in photos if p["id"] in share.get("photo_ids", [])]
    
    return jsonify(sent)


@share_bp.route("/shares/received", methods=["GET"])
def get_received_shares():
    """Get all photos shared TO me by my contacts"""
    user_profile = load_user_profile()
    my_name = user_profile.get("name", "You")
    
    shares = load_shares()
    photos = load_photos()
    
    # Get shares where I'm the recipient (matches contact name to my name)
    received = [s for s in shares if s.get("type") == "received" and s.get("to") == my_name]
    
    for share in received:
        share["photos"] = [p for p in photos if p["id"] in share.get("photo_ids", [])]
    
    return jsonify(received)


@share_bp.route("/shares/contact/<contact_name>", methods=["GET"])
def get_shared_photos(contact_name):
    """Get photos shared WITH a specific contact"""
    shares = load_shares()
    photos = load_photos()
    
    # Find all shares for this contact
    contact_shares = [s for s in shares if s.get("to", "").lower() == contact_name.lower() and s.get("type") == "sent"]
    
    if not contact_shares:
        return jsonify([])
    
    # Gather all photo IDs shared with this contact
    shared_photo_ids = set()
    for share in contact_shares:
        shared_photo_ids.update(share.get("photo_ids", []))
    
    # Get the actual photo objects
    shared_photos = [p for p in photos if p["id"] in shared_photo_ids]
    
    return jsonify(shared_photos)


@share_bp.route("/share/history", methods=["GET"])
def get_share_history():
    """Get complete bidirectional share history"""
    shares = load_shares()
    photos = load_photos()
    
    history = []
    for share in shares:
        share_copy = share.copy()
        share_copy["photos"] = [p for p in photos if p["id"] in share.get("photo_ids", [])]
        history.append(share_copy)
    
    return jsonify(history)
