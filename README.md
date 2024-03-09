## Standup  

> Standup generates a daily standup message summarizing your repos .git history.

### Usage:

First configure the cli:

```
standup configure
```


Then run summarize your git history from `HEAD` to your chosen `git_sha`.

```
standup run <git_sha>
```


### Todos:

* Allow not passing a `git_sha` using a timebased param instead. eg `1 day`. 
* Allow a custom prompt.

### Credits:

Most of the logic was copied or heavily inspired by the [git-llm](https://github.com/rsaryev/git-llm) project.
