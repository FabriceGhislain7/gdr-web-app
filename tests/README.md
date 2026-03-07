# Tests Folder

This folder contains a basic smoke suite to quickly validate core app behavior:

- public pages load (`/`, `/about`, `/guide_game`, `/statistics`, `/login`, `/register`)
- default language is English
- language switch route works (`/set-language/<lang>`)
- analytics route is protected for anonymous users
- analytics page is reachable by developer role

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Notes

- Tests use the current local app configuration and database.
- They are designed to be non-destructive smoke tests.
