from posts.models import Post
from .models import Author
from django.utils import timezone
from deadlybird.util import generate_full_api_url, generate_next_id
from posts.util import send_post_to_inboxes
import requests

AUTHORS_PER_CRON_CHECK = 10

def github_task():
  print("[GITHUB CRON] Starting Task")
  authors = Author.objects.all() \
    .exclude(github=None) \
    .order_by("last_github_check")[:AUTHORS_PER_CRON_CHECK]

  for author in authors:
    url = f"https://api.github.com/users/{author.github}/events"

    last_github_id = author.last_github_id
    latest_github_id = None

    response = requests.get(url=url)
    if not response.ok:
      continue
    
    json = response.json()

    for event in json:      
      if latest_github_id is None:
        latest_github_id = event["id"]

      if event["id"] == last_github_id:
        return

      title = ""
      description = ""
      content = ""

      event_type = event["type"]
      if event_type == "ForkEvent":
        title = "Github - Fork"
        description = f"{event['actor']['display_login']} forked a repository"
        content = f"I forked {event['repo']['name']}. Check it out [here]({event['payload']['forkee']['html_url']})!"
      elif event_type == "PushEvent":
        def commit_to_str(commit):
          return f"- {commit['message']}"
        
        commit_str = "\n".join((map(commit_to_str, event['payload']['commits'])))

        title = "Github - Push"
        description = f"{event['actor']['display_login']} pushed to a repository"
        content = f"I pushed to **{event['repo']['name']}**!\n{commit_str}"
      elif event_type == "WatchEvent":
        title = "Github - Watch"
        description = f"{event['actor']['display_login']} watched a repository"
        content = f"I started watching **{event['repo']['name']}**!"
      elif event_type == "DeleteEvent":
        title = "Github - Delete"
        description = f"{event['actor']['display_login']} deleted from a repository."
        content = f"I deleted a **{event['payload']['ref_type']}** ({event['payload']['ref']})"
      else:
        print(f"[GITHUB CRON] Unknown Github Event: {event_type}")
        continue

      id = generate_next_id()
      Post.objects.create(
        id=id,
        title=title,
        description=description,
        content=content,
        content_type=Post.ContentType.MARKDOWN,
        author=author,
        visibility=Post.Visibility.PUBLIC,
        origin=generate_full_api_url("post", kwargs={ "author_id": author.id, "post_id": id }),
        source=generate_full_api_url("post", kwargs={ "author_id": author.id, "post_id": id }),
      )
      send_post_to_inboxes(id, author.id)

    author.last_github_check = timezone.now()
    author.last_github_id = latest_github_id
    author.save()
  print("[GITHUB CRON] Ending Task")