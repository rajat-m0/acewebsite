from review.models import Review
from ace.settings import BASE_DIR
import json as JSON
from os import path

json = []

for review in Review.objects.all().order_by('submission__user_id'):
    sub = review.submission
    json.append({
        'id' : review.id,
        'reviewed_by' : review.user.name(),
        'name' : sub.user.name(),
        'category' : sub.task.category.name,
        'task' : "{} - {}".format(sub.task.task_name, sub.task.get_difficulty_value_display()),
        'review' : review.feedback,
        'rating' : review.rating,
        'is_selected' : review.is_selected,
    })

with open( path.join(BASE_DIR, 'data.json'), 'w' ) as f:
    JSON.dump(json, f)

