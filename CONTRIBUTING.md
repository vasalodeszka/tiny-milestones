# Contributing to Tiny Milestones

### Helper Scripts
Remove all local branches which have been merged to main:
```bash
git fetch -p && for branch in `git branch -vv | grep ': gone]' | awk '{print $1}'`; do git branch -D $branch; done
```
Add your commit template for conventional commits:
```bash
git config commit.cleanup strip
git config commit.template "$(pwd)/.github/.commit_template"
```
