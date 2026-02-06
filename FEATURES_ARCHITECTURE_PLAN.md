## Features Architecture & Integration Plan

### 1. Reader Analytics Dashboard
- New route: `/analytics/reader` (Flask blueprint)
- Template: `templates/analytics/reader_dashboard.html`
- Service: `app/services/analytics_service.py`
- Integrate with user/book data models for engagement metrics

### 2. Pulse Analysis Engine
- New route: `/analytics/pulse` (Flask blueprint)
- Template: `templates/analytics/pulse_dashboard.html`
- Service: `app/services/pulse_analysis_service.py`
- Real-time analysis logic, visualization (JS/Chart.js or similar)

### 3. Smart Genre Selector
- New route: `/tools/genre-selector` (Flask blueprint)
- Template: `templates/tools/genre_selector.html`
- Service: `app/services/genre_service.py` (AI integration)

### 4. Smart Genre Intelligence Tools
- New route: `/tools/genre-intelligence` (Flask blueprint)
- Template: `templates/tools/genre_intelligence.html`
- Service: `app/services/genre_intelligence_service.py`
- 7 sub-tools as endpoints or AJAX calls

### 5. Brand Kit Creation
- New route: `/tools/brand-kit` (Flask blueprint)
- Template: `templates/tools/brand_kit.html`
- Service: `app/services/brand_kit_service.py`

### 6. EPUB Validator
- New route: `/tools/epub-validator` (Flask blueprint)
- Template: `templates/tools/epub_validator.html`
- Service: `app/services/epub_validator_service.py`
- Integrate EpubCheck (Java subprocess or API)

### 7. Metadata Editor
- New route: `/tools/metadata-editor` (Flask blueprint)
- Template: `templates/tools/metadata_editor.html`
- Service: `app/services/metadata_service.py`
- Edit and validate book metadata

---
Each feature will have its own route, template, and service module for clean separation and maintainability.