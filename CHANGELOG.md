# Changelog

## [0.7.0] - 2025-06-18

### Added
* `submittals`: create endpoint for `get_statuses()`
* `change_events`: create endpoints for `get_statuses()`, `get()`, `show()`, and `find()`
* `change_events.ipynb`: add snippets for change events endpoints

### Changed
* snippets: more testing of companies, projects, and submittals

## [0.6.4] - 2025-05-28

### Added
* `directory.ipynb`: add snippets for trades, users, and vendors directory endpoints in snippet

### Changed
* `procore.py`: update refresh token process so that the submodules are reinitialized with the new access token

## [0.6.3] - 2025-05-13

### Added
* `documents.files`: add `view` parameter to `get()` and `search()` methods
* `documents.files`: add `file_types` parameter to `get()` and `search()` methods
* `documents.files`: add `private` parameter to `get()` method

### Changed
* `base`: remove debug print statements

## [0.6.1] - 2025-05-07

### Added
* `cost_codes`: create endpoint for cost codes: `get()`, `show()`, `find()`, `create()`, `update()`, `delete()` methods

## [0.6.0] - 2025-04-04

### Added
* `permissions`: create endpoint for permissions-related resources: `get()`, `get_company_templates()`, `get_company_template()`, `get_project_templates()` methods
* snippets: add `permissions.ipynb` for snippets

### Changed
* snippets: update cost_codes.ipynb

## [0.5.4] - 2025-02-06

### Added
* `time.timecard`: create `get_for_specified_period()` method to get timecards for a specified period and `party_id`
* `time.timecard`: create `update()` method to patch timecards given their ID and date
* `time.timesheets`: create to house endpoints with "timesheet" specified within them - pulled in functions originally in `time.timecard`

### Changed
* `time.timecard`: change `create_in_project()` to simply `create()` since Procore Developer Support said that using the company-based or project-based timecard endpoint produced the same result
* `tools`: wrap all previous examples into notebook called `generic_tools.ipynb`

### Removed
* `time.timecard`: remove endpoints with "timesheet" 
* `tools`: remove old Python example files

[0.5.4]: https://github.com/rogers-obrien-rad/ProPyCore/releases/tag/v0.5.4
[0.6.0]: https://github.com/rogers-obrien-rad/ProPyCore/releases/tag/v0.6.0