"""
Goal-to-Task Conversion Agent - Streamlit App
Web application that converts user goals into actionable HTML task breakdowns
"""

import streamlit as st
from openai import OpenAI
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Goal-to-Task Converter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# System prompt for the AI agent
SYSTEM_PROMPT = """**ROLE:** You are a Goal-to-Task Conversion Assistant specializing in breaking down any user goal into actionable, achievable tasks

**TASK:** Convert user goals into detailed project plans with smaller achievable tasks organized by timeline, phases, and priorities

**INPUT:** Users will provide their goals in any area - personal, professional, creative, educational, or business objectives like "Learn a new language," "Start a business," or "Get organized"

**OUTPUT:** Generate an HTML response using a professional template structure and styling. Your output must include:
- Modern, elegant CSS styling with a clean color palette
- Color-coded phases (3-5 phases) with circular numbered icons
- Bulleted task lists under each phase (4-8 tasks per phase)
- Professional formatting with smooth hover effects
- Responsive design that works on all devices
- Progress indicators and clear visual hierarchy

**CONSTRAINTS:** 
- Never return plain text - always use HTML format
- Return only the HTML code, do not start or end with markdown code blocks, start directly with <!DOCTYPE html>
- Focus on creating actionable, specific tasks rather than vague suggestions
- Include realistic timelines based on goal complexity (days, weeks, months)
- Ensure tasks build logically toward the main goal
- Keep tasks measurable and achievable
- Each task should start with an action verb
- Use distinct harmonious colors for each phase (blues, greens, purples, oranges, teals)

**STRUCTURE REQUIREMENTS:**
1. Header with goal title and motivational description
2. Timeline overview section
3. 3-5 color-coded phase cards, each with:
   - Circular numbered icon
   - Phase title (2-4 words)
   - Timeline estimate
   - 4-8 specific actionable tasks as bullet points
4. Footer with encouragement message

**STYLING REQUIREMENTS:**
- Professional typography using system fonts
- Card-based layout with shadows
- Hover effects (scale, shadow enhancement)
- Proper spacing and padding
- Color coordination across phases
- Mobile-responsive design
- Clean, modern aesthetic

**CAPABILITIES & REMINDERS:** You can break down complex goals into manageable phases (typically 3-5 phases), suggest realistic timelines, prioritize tasks by importance and dependencies. Always structure tasks logically from initial planning through execution and completion. Make the HTML visually appealing and professional."""


def get_api_key():
    """Get API key from Streamlit secrets"""
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("⚠️ OpenAI API key not found in secrets!")
        st.info("Please configure OPENAI_API_KEY in your Streamlit Cloud secrets settings.")
        return None


def convert_goal_to_tasks(api_key: str, user_goal: str) -> str:
    """Convert a user goal into an HTML task breakdown"""
    try:
        client = OpenAI(api_key=api_key)
        
        with st.spinner("🤖 AI is breaking down your goal into actionable tasks..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_goal}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            html_output = response.choices[0].message.content
            
            # Clean up any markdown code blocks if present
            backticks_html = "```
            backticks = "```"
            
            if html_output.startswith(backticks_html):
                html_output = html_output.replace(backticks_html, "").replace(backticks, "").strip()
            elif html_output.startswith(backticks):
                html_output = html_output.replace(backticks, "").strip()
            
            return html_output
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


def main():
    """Main Streamlit application"""
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🎯 Goal-to-Task Converter</h1>
            <p>Transform any goal into actionable, achievable tasks</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # About section
        st.header("ℹ️ About")
        st.markdown("""
        This app uses OpenAI's GPT-4 to break down your goals into:
        - 3-5 manageable phases
        - Specific actionable tasks
        - Realistic timelines
        - Beautiful HTML output
        
        🔒 API key is securely managed via Streamlit secrets.
        """)
        
        st.markdown("---")
        
        # Example goals
        st.header("💡 Example Goals")
        example_goals = [
            "Learn Spanish in 6 months",
            "Start a YouTube channel",
            "Build a mobile app",
            "Write a novel",
            "Get fit and run a marathon",
            "Launch an online business"
        ]
        
        for goal in example_goals:
            if st.button(goal, key=f"example_{goal}"):
                st.session_state.selected_goal = goal
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Enter Your Goal")
        
        # Use selected goal from sidebar if available
        default_goal = st.session_state.get("selected_goal", "")
        
        user_goal = st.text_area(
            "What do you want to achieve?",
            value=default_goal,
            height=100,
            placeholder="E.g., Learn web development and build my first website",
            help="Enter any personal, professional, creative, or educational goal"
        )
        
        # Generate button
        generate_clicked = st.button("🚀 Generate Task Breakdown", type="primary")
    
    with col2:
        st.subheader("💭 Tips")
        st.markdown("""
        **Be specific:**
        - ✅ "Learn Python for data analysis"
        - ❌ "Learn programming"
        
        **Include timeframe:**
        - ✅ "Get fit in 3 months"
        - ❌ "Get fit"
        
        **Be realistic:**
        - ✅ "Build a portfolio website"
        - ❌ "Build the next Facebook"
        """)
    
    # Process the goal
    if generate_clicked:
        api_key = get_api_key()
        
        if not api_key:
            st.error("⚠️ API key configuration error. Please contact the app administrator.")
        elif not user_goal.strip():
            st.warning("⚠️ Please enter a goal!")
        else:
            # Convert goal to tasks
            html_output = convert_goal_to_tasks(api_key, user_goal.strip())
            
            if html_output:
                st.success("✅ Task breakdown generated successfully!")
                
                # Store in session state
                st.session_state.html_output = html_output
                st.session_state.goal_name = user_goal.strip()
    
    # Display results if available
    if "html_output" in st.session_state:
        st.markdown("---")
        st.subheader("📊 Your Task Breakdown")
        
        # Create tabs for preview and download
        tab1, tab2 = st.tabs(["🖼️ Preview", "💾 Download"])
        
        with tab1:
            # Display HTML in iframe
            st.components.v1.html(st.session_state.html_output, height=800, scrolling=True)
        
        with tab2:
            st.markdown("### Download Your Task Breakdown")
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"goal_breakdown_{timestamp}.html"
            
            # Download button
            st.download_button(
                label="📥 Download HTML File",
                data=st.session_state.html_output,
                file_name=filename,
                mime="text/html",
                help="Download the HTML file to open in your browser"
            )
            
            st.info("💡 **Tip:** Open the downloaded HTML file in any web browser to view your beautiful task breakdown!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 2rem 0;">
            <p>Made with ❤️ using OpenAI GPT-4 and Streamlit</p>
            <p>🔒 Your API key is securely managed and never exposed to users.</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
