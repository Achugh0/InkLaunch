# Manuscript Competition System - InkLaunch

## Overview

The Manuscript Competition System is a fully automated, AI-powered writing contest platform integrated into InkLaunch. It allows administrators to create and manage competitions while authors can submit their manuscripts for automated evaluation.

## Key Features

### For Administrators

1. **Competition Creation**
   - Create competitions with custom titles, descriptions, and genres
   - Set submission windows (start and end dates)
   - Configure evaluation criteria with custom weights
   - Define prize structures for 1st, 2nd, and 3rd place
   - Set entry fees (or make it free)
   - Access: Admin Dashboard → Manage Competitions → Create New Competition

2. **Competition Management**
   - View all competitions (draft, active, closed, evaluating, completed)
   - Publish competitions to accept submissions
   - Close submissions when deadline is reached
   - Trigger AI evaluation of all manuscripts
   - Review AI-generated scores and feedback
   - Select winners manually (with AI recommendations)
   - View submission statistics

3. **AI Evaluation**
   - Automated manuscript evaluation based on:
     * Plot/Story Structure
     * Character Development
     * Writing Quality/Style
     * Originality/Creativity
   - Weighted scoring system
   - Detailed feedback generation
   - Confidence scoring
   - Batch processing of all submissions

### For Authors

1. **Browse Competitions**
   - View all active competitions
   - Filter by genre
   - See submission counts and deadlines
   - Check prize structures
   - Access: Navigation → Writing Contests

2. **Submit Manuscripts**
   - Upload manuscript files (PDF, DOCX, TXT)
   - Provide synopsis and author statement
   - Select genre from competition categories
   - Track submission status
   - View submission history

3. **View Results**
   - See competition winners (after announcement)
   - View own submission status
   - Winners receive detailed feedback
   - Non-winners see generic participation message (as per requirements)

## Competition Workflow

```
1. Draft → Admin creates competition
2. Accepting Submissions → Admin publishes competition
3. Closed → Admin closes submissions (deadline reached)
4. Evaluating → Admin triggers AI evaluation
5. Admin Review → Admin reviews AI scores and selects winners
6. Completed → Winners announced
```

## Database Schema

### Collections

1. **competitions**
   - Basic info, dates, criteria, prizes, status
   
2. **competition_submissions**
   - Manuscript metadata, file paths, author info
   
3. **ai_evaluations**
   - Scores, feedback, strengths, weaknesses
   
4. **competition_winners**
   - Winner records with rankings and prizes

## File Upload

- Manuscripts stored in: `uploads/manuscripts/`
- Supported formats: PDF, DOCX, DOC, TXT
- Naming convention: `{user_id}_{competition_id}_{timestamp}_{filename}`

## AI Evaluation Criteria

Default evaluation weights:
- **Plot Structure**: 25%
- **Character Development**: 25%
- **Writing Quality**: 25%
- **Originality**: 25%

Admins can customize these weights when creating competitions.

## API Endpoints

### Admin Routes (`/admin/competitions`)
- `GET /` - List all competitions
- `GET/POST /create` - Create new competition
- `GET /<id>` - View competition details
- `POST /<id>/publish` - Publish competition
- `POST /<id>/close` - Close submissions
- `POST /<id>/evaluate` - Start AI evaluation
- `GET/POST /<id>/select-winners` - Select and announce winners
- `GET/POST /<id>/edit` - Edit draft competition

### Author Routes (`/manuscript-competitions`)
- `GET /` - Browse competitions
- `GET /<id>` - View competition details
- `GET/POST /<id>/submit` - Submit manuscript
- `GET /my-submissions` - View own submissions
- `GET /my-wins` - View own wins

## Future Enhancements (Phase 2+)

- [ ] Payment gateway integration for entry fees
- [ ] Email notifications for winners and participants
- [ ] Plagiarism detection
- [ ] Multiple evaluation rounds
- [ ] Public voting component
- [ ] Winner certificates generation
- [ ] Competition analytics dashboard
- [ ] Genre-specific evaluation models
- [ ] Manuscript preview/download for admins
- [ ] Automated deadline closure (cron jobs)

## Testing the System

### As Admin:
1. Login as admin
2. Navigate to Admin Dashboard
3. Click "Manage Competitions"
4. Create a new competition
5. Publish it
6. (After submissions) Close and evaluate
7. Select winners

### As Author:
1. Register/login as regular user
2. Click "Writing Contests" in navigation
3. Browse active competitions
4. Click "View Details & Submit"
5. Fill out submission form and upload manuscript
6. Check "My Submissions" for status

## Technical Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **AI**: OpenAI GPT-4 (via `ai_service.py`)
- **File Handling**: Werkzeug secure_filename
- **Frontend**: Bootstrap 5, Jinja2 templates

## Configuration

Required config variables (already set):
- `OPENAI_API_KEY` - For AI evaluations
- `AI_MODEL` - GPT model to use (default: gpt-4)
- `UPLOAD_FOLDER` - Where to store manuscripts

## Security Considerations

- File upload validation (extension whitelist)
- Secure filename generation
- Admin-only competition management
- Author can only see own submissions
- MongoDB ObjectId validation
- No manuscript content visible to authors (only synopsis used for display)

---

**Built for InkLaunch - Empowering Authors**
