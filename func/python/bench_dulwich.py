import os

import dulwich.repo


def faasm_main():
    if os.environ.get("PYTHONWASM") == "1":
        repo_path = "/lib/python3.8/site-packages/pyperformance/benchmarks/data/asyncio.git"
    else:
        repo_path = "/code/cpp/venv/lib/python3.8/site-packages/pyperformance/benchmarks/data/asyncio.git"

    repo = dulwich.repo.Repo(repo_path)
    head = repo.head()

    # Iterate on all changes on the Git repository
    for _ in repo.get_walker(head):
        pass

    repo.close()

    return 0


if __name__ == "__main__":
    faasm_main()
