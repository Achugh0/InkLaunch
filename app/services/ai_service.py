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
