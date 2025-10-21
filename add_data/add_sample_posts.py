
from app import create_app
from app.extensions import db
from app.models.posts import BlogPost
from app.models.user import User
from app.models.category import Category
from datetime import datetime, timedelta
import random

def add_sample_posts():
    app = create_app()
    
    with app.app_context():
        # Check if we have any users first
        users = User.query.all()
        if not users:
            print("No users found. Creating a sample user first...")
            # Create a sample user
            sample_user = User(
                username="admin",
                email="admin@example.com",
                avatar="userImg/default-user.jpg"
            )
            sample_user.set_password("password123")
            db.session.add(sample_user)
            db.session.commit()
            users = [sample_user]
        
        # Sample posts data
        sample_posts = [
            {
                "title": "Getting Started with Python Web Development",
                "excerpt": "Learn the fundamentals of building web applications with Python and Flask framework.",
                "content": """
                <p>Python web development has become increasingly popular due to its simplicity and powerful frameworks. In this comprehensive guide, we'll explore the fundamentals of building web applications using Python.</p>
                
                <h3>Why Choose Python for Web Development?</h3>
                <p>Python offers several advantages for web development:</p>
                <ul>
                    <li>Clean and readable syntax</li>
                    <li>Extensive library ecosystem</li>
                    <li>Strong community support</li>
                    <li>Rapid development capabilities</li>
                </ul>
                
                <h3>Popular Python Web Frameworks</h3>
                <p>Flask and Django are the most popular Python web frameworks, each with their own strengths and use cases.</p>
                
                <p>Flask is lightweight and flexible, making it perfect for small to medium applications, while Django provides a more comprehensive solution with built-in features.</p>
                """,
                "category": "Programming",
                "meta_description": "Complete guide to Python web development with Flask framework for beginners",
                "thumbnail": "userImg/default-user.jpg",
                "status": "published"
            },
            {
                "title": "The Future of Artificial Intelligence",
                "excerpt": "Exploring the latest trends and developments in AI technology and their impact on society.",
                "content": """
                <p>Artificial Intelligence is transforming every aspect of our lives, from healthcare to transportation, and everything in between.</p>
                
                <h3>Current AI Trends</h3>
                <p>Some of the most significant AI trends include:</p>
                <ul>
                    <li>Machine Learning and Deep Learning</li>
                    <li>Natural Language Processing</li>
                    <li>Computer Vision</li>
                    <li>Autonomous Systems</li>
                </ul>
                
                <h3>Impact on Industries</h3>
                <p>AI is revolutionizing industries by automating processes, improving efficiency, and enabling new capabilities that were previously impossible.</p>
                
                <p>From medical diagnosis to financial trading, AI is becoming an integral part of modern business operations.</p>
                """,
                "category": "Technology",
                "meta_description": "Explore the future of AI technology and its impact on various industries",
                "thumbnail": "userImg/default-user.jpg",
                "status": "published"
            },
            {
                "title": "Healthy Lifestyle Tips for Busy Professionals",
                "excerpt": "Practical advice for maintaining a healthy lifestyle while managing a demanding career.",
                "content": """
                <p>Maintaining a healthy lifestyle while juggling a busy professional career can be challenging, but it's not impossible.</p>
                
                <h3>Time Management for Health</h3>
                <p>The key to a healthy lifestyle as a busy professional is efficient time management:</p>
                <ul>
                    <li>Schedule workout sessions like important meetings</li>
                    <li>Meal prep on weekends</li>
                    <li>Use technology to track habits</li>
                    <li>Set realistic goals</li>
                </ul>
                
                <h3>Quick Healthy Habits</h3>
                <p>Small changes can make a big difference in your overall health and wellbeing.</p>
                
                <p>Simple habits like taking the stairs, drinking more water, and getting adequate sleep can significantly improve your quality of life.</p>
                """,
                "category": "Health",
                "meta_description": "Essential health tips for busy professionals to maintain wellness",
                "thumbnail": "userImg/default-user.jpg",
                "status": "published"
            },
            {
                "title": "Building a Successful Startup: Lessons Learned",
                "excerpt": "Key insights and practical advice from successful entrepreneurs on building a thriving startup.",
                "content": """
                <p>Starting a successful business requires more than just a great idea. It demands persistence, strategic thinking, and the ability to adapt quickly.</p>
                
                <h3>Essential Startup Principles</h3>
                <p>Here are the fundamental principles every entrepreneur should know:</p>
                <ul>
                    <li>Validate your idea early and often</li>
                    <li>Focus on solving real problems</li>
                    <li>Build a strong team</li>
                    <li>Manage cash flow carefully</li>
                </ul>
                
                <h3>Common Mistakes to Avoid</h3>
                <p>Learning from others' mistakes can save you time and money in your entrepreneurial journey.</p>
                
                <p>Many startups fail due to lack of market research, poor financial planning, or trying to do too much too quickly.</p>
                """,
                "category": "Business",
                "meta_description": "Startup advice and lessons learned from successful entrepreneurs",
                "thumbnail": "userImg/default-user.jpg",
                "status": "published"
            },
            {
                "title": "Modern Web Design Trends for 2024",
                "excerpt": "Discover the latest web design trends that are shaping the digital landscape this year.",
                "content": """
                <p>Web design continues to evolve rapidly, with new trends emerging that focus on user experience, accessibility, and visual appeal.</p>
                
                <h3>Top Design Trends</h3>
                <p>The most influential design trends for 2024 include:</p>
                <ul>
                    <li>Minimalist and clean interfaces</li>
                    <li>Dark mode implementations</li>
                    <li>Interactive animations</li>
                    <li>Bold typography choices</li>
                </ul>
                
                <h3>User Experience Focus</h3>
                <p>Modern web design prioritizes user experience above all else, ensuring that websites are not only beautiful but also functional and accessible.</p>
                
                <p>Responsive design and mobile-first approaches are no longer optional but essential for any successful web presence.</p>
                """,
                "category": "Design",
                "meta_description": "Latest web design trends and best practices for 2024",
                "thumbnail": "userImg/default-user.jpg",
                "status": "published"
            },
            {
                "title": "Remote Work Best Practices",
                "excerpt": "Essential tips and strategies for maximizing productivity while working from home.",
                "content": """
                <p>Remote work has become the new normal for many professionals, bringing both opportunities and challenges.</p>
                
                <h3>Setting Up Your Home Office</h3>
                <p>A productive remote work environment requires:</p>
                <ul>
                    <li>Dedicated workspace</li>
                    <li>Ergonomic furniture</li>
                    <li>Reliable internet connection</li>
                    <li>Proper lighting</li>
                </ul>
                
                <h3>Maintaining Work-Life Balance</h3>
                <p>One of the biggest challenges of remote work is maintaining boundaries between work and personal life.</p>
                
                <p>Establishing clear schedules, taking regular breaks, and creating physical separation between work and leisure spaces are crucial for long-term success.</p>
                """,
                "category": "Lifestyle",
                "meta_description": "Complete guide to remote work productivity and work-life balance",
                "thumbnail": "userImg/default-user.jpg",
                "status": "published"
            }
        ]

        for data in sample_posts:
            # create category if not exists with name, icom, description
            category_icons = {
                    'Technology': 'laptop',
                    'Lifestyle': 'heart',
                    'Travel': 'geo-alt',
                    'Business': 'graph-up',
                    'Health': 'activity',
                    'Education': 'book',
                    'Design': 'palette',
                    'Programming': 'code-slash'
            }
            category = Category.query.filter_by(name=data["category"]).first()
            if not category:
                category = Category(name=data["category"], icon=category_icons[data["category"]], description=data["category"])
                db.session.add(category)
                db.session.commit()
        
        # Generate slugs and add posts
        for i, post_data in enumerate(sample_posts):
            # Create slug from title
            slug = post_data["title"].lower()
            slug = slug.replace(" ", "-")
            slug = "".join(c for c in slug if c.isalnum() or c == "-")
            
            # Check if post already exists
            existing_post = BlogPost.query.filter_by(slug=slug).first()
            if existing_post:
                print(f"Post with slug '{slug}' already exists, skipping...")
                continue
            
            category = Category.query.filter_by(name=post_data["category"]).first_or_404()
            post_data["category_id"] = category.id
            # Create random publish date within last 30 days
            days_ago = random.randint(1, 30)
            publish_date = datetime.utcnow() - timedelta(days=days_ago)
            
            # Create the blog post
            new_post = BlogPost(
                title=post_data["title"],
                excerpt=post_data["excerpt"],
                slug=slug,
                content=post_data["content"],
                category_id=post_data["category_id"],
                meta_description=post_data["meta_description"],
                thumbnail=post_data["thumbnail"],
                status=post_data["status"],
                views=random.randint(10, 500),
                comments_count=0,
                publish_date=publish_date,
                created_at=publish_date,
                user_id=random.choice(users).id
            )
            
            db.session.add(new_post)
            print(f"Added post: {post_data['title']}")
        
        # Commit all changes
        db.session.commit()
        print(f"\nSuccessfully added {len(sample_posts)} sample posts to the database!")
        
        # Display summary
        total_posts = BlogPost.query.count()
        print(f"Total posts in database: {total_posts}")

if __name__ == "__main__":
    add_sample_posts()
