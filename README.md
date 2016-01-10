# github-clone
A script to automatic set "upstream" remote to parent in GitHub

# Installation

1. ```git clone https://github.com/ad-m/github-clone.git github-clone```
2. ```sudo pip install -R github-clone/requirements.txt```
3. ```git config --global alias.gh "!python {path}/clone-github.py"```

# Usage

```
git gh [git_url] [output_dir]
```

# Example
```
git gh git@github.com:ad-m/github-clone.git github-clone
git gh https://github.com/ad-m/github-clone.git github-clone
```
