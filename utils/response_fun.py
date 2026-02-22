from utils.user_preview import get_user_preview

def enrich_post(post, user_id):
    likes = post.get("likes", [])
    saved = post.get("savedBy", [])

    return {
        "_id": str(post["_id"]),
        "caption": post.get("caption"),
        "image": post.get("image"),
        "video": post.get("video"),

        "author": get_user_preview(post["author"]),

        "likesCount": len(likes),
        "savedCount": len(saved),
        "commentsCount": post.get("commentsCount", 0),

        "likes": user_id in [str(u) for u in likes],
        "savedBy": user_id in [str(u) for u in saved],

        "createdAt": post["createdAt"]
    }