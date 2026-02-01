# PowerShell script to automatically add, commit, and push all changes to git
# Usage: Run this script in your repository directory

# Add all changes
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    # Commit with a timestamp message
    $commitMessage = "Auto commit on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git commit -m $commitMessage
    
    # Push to the current branch's upstream
    git push
    Write-Host "Successfully pushed changes to git!"
} else {
    Write-Host "No changes to commit."
}