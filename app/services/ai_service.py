"""AI Service for book reviews using OpenAI GPT-4."""
import openai
import time
from flask import current_app


class AIService:
    """AI service for book analysis."""
    
    def __init__(self):
        """Initialize AI service."""
        openai.api_key = current_app.config['OPENAI_API_KEY']
        self.model = current_app.config['AI_MODEL']
    
    def review_book(self, book, nomination, author):
        """Generate AI review for a book."""
        start_time = time.time()
        
        # Prepare prompt
        prompt = self._prepare_prompt(book, nomination, author)
        
        try:
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert literary critic and book analyst. Provide detailed, constructive analysis of books across multiple dimensions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            processing_time = time.time() - start_time
            
            # Parse response
            content = response.choices[0].message.content
            
            # Extract scores and analysis
            review_data = self._parse_review(content)
            review_data['processing_time_seconds'] = round(processing_time, 2)
            review_data['tokens_used'] = response.usage.total_tokens
            review_data['ai_model'] = self.model
            
            return review_data
            
        except Exception as e:
            raise Exception(f"AI review failed: {str(e)}")
    
    def _prepare_prompt(self, book, nomination, author):
        """Prepare prompt for AI review."""
        return f"""
Please provide a comprehensive analysis of the following book submission for our "Author of the Month" competition.

**Book Information:**
- Title: {book.get('title')}
- Subtitle: {book.get('subtitle', 'N/A')}
- Genre: {book.get('genre')}
- Author: {author.get('full_name')}
- Page Count: {book.get('page_count', 'N/A')}
- Language: {book.get('language', 'English')}

**Description:**
{book.get('description')}

**Nomination Statement:**
{nomination.get('nomination_statement')}

**Author Bio:**
{author.get('bio', 'Not provided')}

Please evaluate this book across the following dimensions and provide scores from 1-10 (with one decimal place):

1. **Content Quality** (25% weight): Plot/narrative strength, character development, information depth, structure, coherence
2. **Writing Style** (25% weight): Prose quality, voice and tone, pacing, dialogue, descriptive language
3. **Originality** (20% weight): Unique perspective, fresh concepts, differentiation from existing works
4. **Market Potential** (15% weight): Target audience size, commercial viability, market demand
5. **Technical Quality** (15% weight): Grammar, spelling, formatting, professional presentation

Provide your analysis in the following format:

SCORES:
Content Quality: [score]
Writing Style: [score]
Originality: [score]
Market Potential: [score]
Technical Quality: [score]

OVERALL RATING: [weighted average score]

SUMMARY:
[200-300 word professional assessment]

STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]

WEAKNESSES:
- [weakness 1]
- [weakness 2]
- [weakness 3]

RECOMMENDATIONS:
[Constructive suggestions for improvement]

TARGET AUDIENCE:
[Demographic and psychographic profile]

COMPARABLE TITLES:
- [title 1]
- [title 2]
- [title 3]

KEY THEMES:
[Primary topics and concepts]

GENRE ALIGNMENT:
[How well the book fits its declared genre]

READABILITY:
[Accessibility assessment]

SENTIMENT:
[Overall emotional tone]
"""
    
    def _parse_review(self, content):
        """Parse AI review response."""
        lines = content.split('\n')
        
        review_data = {
            'content_quality_score': 0.0,
            'writing_style_score': 0.0,
            'originality_score': 0.0,
            'market_potential_score': 0.0,
            'technical_quality_score': 0.0,
            'overall_rating': 0.0,
            'review_summary': '',
            'strengths': [],
            'weaknesses': [],
            'recommendations': '',
            'target_audience': '',
            'comparable_titles': [],
            'key_themes': [],
            'genre_alignment': '',
            'readability_score': '',
            'sentiment_analysis': ''
        }
        
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Check for sections
            if 'SCORES:' in line:
                current_section = 'scores'
            elif 'OVERALL RATING:' in line:
                try:
                    rating = float(line.split(':')[1].strip())
                    review_data['overall_rating'] = rating
                except:
                    pass
            elif 'SUMMARY:' in line:
                current_section = 'summary'
                section_content = []
            elif 'STRENGTHS:' in line:
                if section_content:
                    review_data['review_summary'] = ' '.join(section_content)
                current_section = 'strengths'
                section_content = []
            elif 'WEAKNESSES:' in line:
                current_section = 'weaknesses'
                section_content = []
            elif 'RECOMMENDATIONS:' in line:
                current_section = 'recommendations'
                section_content = []
            elif 'TARGET AUDIENCE:' in line:
                if section_content:
                    review_data['recommendations'] = ' '.join(section_content)
                current_section = 'target_audience'
                section_content = []
            elif 'COMPARABLE TITLES:' in line:
                if section_content:
                    review_data['target_audience'] = ' '.join(section_content)
                current_section = 'comparable_titles'
                section_content = []
            elif 'KEY THEMES:' in line:
                current_section = 'key_themes'
                section_content = []
            elif 'GENRE ALIGNMENT:' in line:
                if section_content:
                    review_data['key_themes'] = section_content
                current_section = 'genre_alignment'
                section_content = []
            elif 'READABILITY:' in line:
                if section_content:
                    review_data['genre_alignment'] = ' '.join(section_content)
                current_section = 'readability'
                section_content = []
            elif 'SENTIMENT:' in line:
                if section_content:
                    review_data['readability_score'] = ' '.join(section_content)
                current_section = 'sentiment'
                section_content = []
            elif current_section == 'scores':
                # Parse individual scores
                if 'Content Quality:' in line:
                    try:
                        review_data['content_quality_score'] = float(line.split(':')[1].strip())
                    except:
                        pass
                elif 'Writing Style:' in line:
                    try:
                        review_data['writing_style_score'] = float(line.split(':')[1].strip())
                    except:
                        pass
                elif 'Originality:' in line:
                    try:
                        review_data['originality_score'] = float(line.split(':')[1].strip())
                    except:
                        pass
                elif 'Market Potential:' in line:
                    try:
                        review_data['market_potential_score'] = float(line.split(':')[1].strip())
                    except:
                        pass
                elif 'Technical Quality:' in line:
                    try:
                        review_data['technical_quality_score'] = float(line.split(':')[1].strip())
                    except:
                        pass
            elif current_section in ['summary', 'recommendations', 'target_audience', 'genre_alignment', 'readability', 'sentiment']:
                section_content.append(line)
            elif current_section == 'strengths' and line.startswith('-'):
                review_data['strengths'].append(line[1:].strip())
            elif current_section == 'weaknesses' and line.startswith('-'):
                review_data['weaknesses'].append(line[1:].strip())
            elif current_section == 'comparable_titles' and line.startswith('-'):
                review_data['comparable_titles'].append(line[1:].strip())
            elif current_section == 'key_themes':
                section_content.append(line)
        
        # Handle last section
        if current_section == 'sentiment' and section_content:
            review_data['sentiment_analysis'] = ' '.join(section_content)
        
        # Calculate overall rating if not provided
        if review_data['overall_rating'] == 0.0:
            weights = {
                'content_quality_score': 0.25,
                'writing_style_score': 0.25,
                'originality_score': 0.20,
                'market_potential_score': 0.15,
                'technical_quality_score': 0.15
            }
            total = sum(review_data[key] * weight for key, weight in weights.items())
            review_data['overall_rating'] = round(total, 1)
        
        return review_data


def evaluate_manuscript(manuscript_title, synopsis, word_count, genre, criteria):
    """
    Evaluate a manuscript submission for competition using AI.
    
    Args:
        manuscript_title: Title of the manuscript
        synopsis: Synopsis/summary of the manuscript
        word_count: Word count
        genre: Genre of the manuscript
        criteria: Dictionary of evaluation criteria with weights
    
    Returns:
        Dictionary with evaluation results
    """
    import openai
    from flask import current_app
    
    start_time = time.time()
    
    # Prepare prompt based on criteria
    criteria_list = []
    for criterion, weight in criteria.items():
        criteria_list.append(f"- {criterion.replace('_', ' ').title()}: {weight}% weight")
    
    criteria_text = '\n'.join(criteria_list)
    
    prompt = f"""You are an expert literary critic evaluating a {genre} manuscript for a writing competition.

**Manuscript Information:**
- Title: {manuscript_title}
- Genre: {genre}
- Word Count: {word_count:,}

**Synopsis:**
{synopsis}

**Evaluation Criteria (with weights):**
{criteria_text}

Please evaluate this manuscript across each criterion and provide scores from 1-10 (where 1-2 is Poor, 3-4 is Below Average, 5-6 is Average, 7-8 is Good, 9-10 is Excellent).

Provide your evaluation in the following format:

CRITERION SCORES:
{chr(10).join(f"{c.replace('_', ' ').title()}: [score] - [brief 1-sentence justification]" for c in criteria.keys())}

WEIGHTED OVERALL SCORE: [calculated weighted average]

CONFIDENCE: [1-10 score indicating your confidence in this evaluation]

STRENGTHS:
- [Strength 1]
- [Strength 2]
- [Strength 3]

WEAKNESSES:
- [Weakness 1]
- [Weakness 2]
- [Weakness 3]

DETAILED FEEDBACK:
[2-3 paragraph comprehensive feedback explaining your evaluation, highlighting what works well and what could be improved. Be constructive and specific.]
"""
    
    try:
        openai.api_key = current_app.config.get('OPENAI_API_KEY')
        model = current_app.config.get('AI_MODEL', 'gpt-4')
        
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert literary critic evaluating manuscripts for writing competitions. Provide fair, constructive, and detailed analysis."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        processing_time = time.time() - start_time
        content = response.choices[0].message.content
        
        # Parse response
        lines = content.split('\n')
        criteria_scores = {}
        overall_score = 0.0
        confidence_score = 8.0
        strengths = []
        weaknesses = []
        detailed_feedback = ""
        
        current_section = None
        feedback_lines = []
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('CRITERION SCORES:'):
                current_section = 'criteria'
                continue
            elif line.startswith('WEIGHTED OVERALL SCORE:'):
                try:
                    overall_score = float(line.split(':')[1].strip().split()[0])
                except:
                    pass
                continue
            elif line.startswith('CONFIDENCE:'):
                try:
                    confidence_score = float(line.split(':')[1].strip().split()[0])
                except:
                    pass
                continue
            elif line.startswith('STRENGTHS:'):
                current_section = 'strengths'
                continue
            elif line.startswith('WEAKNESSES:'):
                current_section = 'weaknesses'
                continue
            elif line.startswith('DETAILED FEEDBACK:'):
                current_section = 'feedback'
                continue
            
            if current_section == 'criteria' and ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    criterion_name = parts[0].strip().lower().replace(' ', '_')
                    try:
                        score = float(parts[1].strip().split()[0])
                        criteria_scores[criterion_name] = score
                    except:
                        pass
            elif current_section == 'strengths' and line.startswith('-'):
                strengths.append(line[1:].strip())
            elif current_section == 'weaknesses' and line.startswith('-'):
                weaknesses.append(line[1:].strip())
            elif current_section == 'feedback' and line:
                feedback_lines.append(line)
        
        detailed_feedback = ' '.join(feedback_lines)
        
        # Calculate weighted score if not provided
        if overall_score == 0.0:
            total = 0.0
            for criterion, weight in criteria.items():
                criterion_key = criterion.lower().replace(' ', '_')
                if criterion_key in criteria_scores:
                    total += criteria_scores[criterion_key] * (weight / 100.0)
            overall_score = round(total, 2)
        
        return {
            'model_version': model,
            'criteria_scores': criteria_scores,
            'overall_score': overall_score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'detailed_feedback': detailed_feedback,
            'confidence_score': confidence_score,
            'processing_time': round(processing_time, 2)
        }
        
    except Exception as e:
        raise Exception(f"Manuscript evaluation failed: {str(e)}")

