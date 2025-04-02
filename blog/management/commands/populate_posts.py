from blog.models import Post,Category
from django.core.management.base import BaseCommand
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = "Insert sample data into the Post model"

    def handle(self, *args, **options):



        titles = [
                "Global Markets Rally as Inflation Cools",
                "Tech Giants Announce Breakthrough AI Innovations",
                "New Study Reveals Impact of Climate Change on Oceans",
                "Government Unveils New Tax Reforms",
                "Major Cybersecurity Breach Exposes Millions of Records",
                "Scientists Discover New Exoplanet with Earth-like Conditions",
                "SpaceX Successfully Launches Next-Gen Satellite",
                "Stock Market Sees Record Highs Amid Economic Recovery",
                "Breakthrough in Cancer Treatment Raises Hope",
                "International Summit Focuses on Renewable Energy",
                "New Legislation Aims to Improve Data Privacy",
                "AI-Powered Robots Transform Manufacturing Industry",
                "FIFA World Cup 2026 Qualifiers: Key Matches This Week",
                "Scientists Develop Sustainable Plastic Alternative",
                "Global Supply Chain Challenges Continue in 2025",
                "Electric Vehicles Outsell Gasoline Cars for First Time",
                "Major Tech Firm Faces Antitrust Investigation",
                "Astronomers Detect Signals from Deep Space",
                "World Leaders Meet to Address Global Water Crisis",
                "New Smartphone Model Boasts Revolutionary Camera Tech",

        ]

        contents = [
                        "A leading technology company has launched a cutting-edge smartphone that leverages artificial intelligence (AI) to provide users with an unparalleled mobile experience.",
                        "A groundbreaking discovery has been made by a team of scientists who have identified a new planet with conditions that could support life.",
                        "A major medical breakthrough has been achieved with the development of a novel cancer treatment.",
                        "In an electrifying finale, a sports team has emerged victorious, claiming the championship title in their respective league.",
                        "The government has unveiled a comprehensive set of policies aimed at mitigating the effects of climate change.",
                        "The cryptocurrency market has witnessed significant volatility this week, with major cryptocurrencies experiencing substantial price swings",
                        "A team of researchers has made a pioneering breakthrough in the field of renewable energy, developing a novel technology that harnesses energy from an innovative source.",
                        "The entertainment industry has experienced a notable surge in streaming service subscriptions, as more consumers turn to online platforms for their entertainment needs.",
                        "A groundbreaking space mission has achieved a major milestone by successfully landing on Mars",
                        "Cybersecurity experts have issued a warning about an emerging wave of online threats, including sophisticated malware, phishing attacks, and ransomware.",
                        "Major automakers have unveiled new electric vehicle (EV) models that boast improved range, performance, and efficiency.",
                        "The education system is undergoing significant reforms aimed at improving accessibility, affordability, and quality of education for all students.",
                        "A team of scientists has made a groundbreaking discovery by developing a revolutionary vaccine for a rare and debilitating disease.",
                        "A major corporation is facing legal challenges and scrutiny over data privacy concerns, highlighting the need for stronger data protection regulations",
                        "A highly anticipated Hollywood film has shattered box office records worldwide, grossing millions of dollars in its opening weekend.",
                        "Hollywood blockbuster breaks box office records worldwide.Artificial intelligence (AI)-powered robots are revolutionizing various industries, including manufacturing, healthcare, and logistics, at an unprecedented pace.",
                        "Several major tech companies have formed an alliance aimed at improving internet security, protecting user data, and preventing cyber threats.",
                        "Health experts are emphasizing the importance of mental wellness programs, highlighting the need for greater awareness, support, and resources to address mental health issues.",
                        "A significant breakthrough has been achieved in quantum computing, setting new benchmarks in technology and paving the way for faster, more secure, and more powerful computing capabilities.",
                        "Major automakers have unveiled new electric vehicle (EV) models that boast improved range, performance"

        ]

        image_urls = [f"https://picsum.photos/id/{i}/800/400" for i in range(100, 121)]

        categories = Category.objects.all()

        for title, content, image_url in zip(titles, contents, image_urls):
            category = random.choice(categories)
            if not Post.objects.filter(title=title).exists():
                post = Post(title=title, content=content, image_url=image_url,category=category)
                post.save()

        self.stdout.write(self.style.SUCCESS("Successfully inserted sample posts"))
