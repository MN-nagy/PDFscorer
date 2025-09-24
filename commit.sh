#!/bin/zsh
# Use provided commit message, or default to "Tests passed"
if [[ -n "$1" ]]; then
    commit_message="$1"
else
    commit_message="Tests passed"
fi

# Detect the root of the git repository
git_root=$(git rev-parse --show-toplevel 2>/dev/null)

if [[ -z "$git_root" ]]; then
    echo "Not inside a Git repository."
    exit 1
fi

lock_file_path="$git_root/.git/index.lock"

# Function to perform git add and commit
function git_add_commit() {
    git add . && git commit -m "$commit_message"
}

echo "Attempting git add and commit..."
if ! git_add_commit; then
    if [[ -f "$lock_file_path" ]]; then
        echo "Detected Git lock file issue: $lock_file_path"
        echo "Attempting to remove the lock file and retry the commit."
        rm "$lock_file_path" && echo "Lock file removed successfully."

        echo "Retrying git add and commit..."
        if ! git_add_commit; then
            echo "Retry failed during git add/commit."
            exit 1
        fi
    else
        echo "git add/commit failed for unknown reasons."
        exit 1
    fi
fi

echo "Attempting git push..."
if ! git push; then
    echo "Git push failed."
    exit 1
fi

echo "Git commit and push completed successfully."
