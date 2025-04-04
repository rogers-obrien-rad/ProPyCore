# Changelog

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