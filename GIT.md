# Setup
 - Install git by following the instructions at https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
 - Install a diff tool and set it. `meld` is a good choice on linux. 
   - `git config --global merge.tool meld`
 - Tell Git which editor to use. Run `git config --global core.editor <editor>`. `nano` or `vi` are good choices.
 - Configure name and email
   ```
    git config --global user.name "gerdogan"
    git config --global user.email gokererdogan@gmail.com
   ```
- Tell Git to ignore certain files. You can set this for each project by creating a `.gitignore` file in project folder. For example to ignore `tmp` files, add line `*.mcmc` to `.gitignore` file. You can also ignore folders by adding the folder name with a trailing slash, `folder/`. In order to set Git to ignore some files globally, create `.gitignore` file in home folder and tell Git about it.
   ```
   # Create a ~/.gitignore in your user directory
   cd ~/
   touch .gitignore
   # Exclude pyc files
   echo "*.pyc" >> .gitignore
   # Configure Git to use this file
   # as global .gitignore
   git config --global core.excludesfile ~/.gitignore 
   ```

# Creating a repository
 - Create a folder on your computer for your code.
 - Run `git init` (in the folder) to initialize a repository inside that folder.
 - Create the repo on github and link your local repo to it.
   - Go to github and press + on the top right and create a new repository.
   - Copy the `git remote add` command and run it on your computer in your code folder.
   - This links your local folder with the remote repo on github.

# Simple workflow
 - Work on your code, make changes.
 - Once ready to commit these,
   - Run `git status` to see what is tracked/untracked.
   - Run `git add <file>` or `git add .` (to add all files).
   - Run `git commit`, write a commit message and save the file. This will commit all added changes. If you leave the message empty, no changes are committed.
   - Push the changes to github with `git push`.
     - First time you run this, git will complain because it does not know where to push this branch. 
     - Tell the name of the remote branch with `git push --set-upstream <remote_name> <branch>`. 
 - To get the latest changes from remote, run `git pull`.

# Branches 
 - You can create a branch using `git branch branchname`.
 - Default branch is named `master`. 
 - List branches with `git branch`.
 - Switch to another branch using `git checkout <branch_name>`.
 - Delete a branch with `git branch -d branchname`.
 - Merge branch <x> to branch <y> with
   ```
   git checkout <y> # switch to branch y
   git merge <x> # merge x to y 
   ```
