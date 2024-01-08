import os
import itertools
from datetime import datetime, timedelta
from github import Github

def create_rotation_schedule(team_members, rotation_interval_weeks):
    rotation_schedule = {}
    rotation_order = itertools.cycle(team_members)

    current_date = datetime.now()

    for week_number in range(1, 53):  # Assuming 52 weeks in a year
        current_member = next(rotation_order)
        rotation_schedule[current_date] = current_member
        current_date += timedelta(weeks=rotation_interval_weeks)

    return rotation_schedule

def main():
    # GitHub token for authentication
    github_token = os.environ.get('GITHUB_TOKEN')
    g = Github(github_token)

    # Your team members
    team_members = ["Alice", "Bob", "Charlie", "David", "Eve"]

    # Rotation interval in weeks
    rotation_interval_weeks = 1

    # Get the repository
    repo = g.get_repo("your-username/your-repo")

    # Create the rotation schedule
    schedule = create_rotation_schedule(team_members, rotation_interval_weeks)

    # Get the next reviewer for the current week
    current_date = datetime.now()
    current_reviewer = schedule[current_date]

    # Assign the reviewer to the pull requests
    open_pull_requests = repo.get_pulls(state='open')
    for pr in open_pull_requests:
        pr.create_review_request(reviewers=[current_reviewer])

if __name__ == "__main__":
    main()
