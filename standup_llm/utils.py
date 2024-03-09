from typing import TypedDict, List
from git import Commit, Repo

class Log(TypedDict):
    commit: Commit 
    diffs: str 

class Git:
    def __init__(self, path: str =''):
        self.repo = Repo(path=path, search_parent_directories=True)
        if not self.has_repository():
            raise Exception("🤖 No git repository found")

    def has_repository(self):
        return self.repo.bare is False

    def logs(self, target_sha: str) -> List[Log]:  
        logs: List[Log] = []
        commits = list(self.repo.iter_commits('HEAD', max_count=50))

        filtered_commits = []
        for commit in commits:
            filtered_commits.append(commit)
            if commit.hexsha == target_sha:
                break

        for commit in filtered_commits:
            if commit.parents:
                diff_body = []
                diffs = commit.diff(commit.parents[0], create_patch=True)
                for diff in diffs:
                    diff_body.append(diff.diff.decode('utf-8'))

                logs.append({ "commit": commit, "diffs": "\n".join(diff_body)})
            else:
                logs.append({ "commit": commit, "diffs": "" })

        return logs
