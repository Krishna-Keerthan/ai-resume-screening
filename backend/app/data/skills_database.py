# backend/app/data/skills_database.py

SKILLS_DATABASE = {
    # Programming Languages
    'programming_languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php',
        'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'perl',
        'objective-c', 'dart', 'elixir', 'haskell', 'lua', 'shell', 'bash'
    ],
    
    # Web Development
    'web_frameworks': [
        'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask',
        'spring', 'asp.net', 'laravel', 'rails', 'nextjs', 'nuxt', 'svelte',
        'fastapi', 'nestjs', 'ember'
    ],
    
    # Databases
    'databases': [
        'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle',
        'sql server', 'sqlite', 'dynamodb', 'elasticsearch', 'neo4j',
        'mariadb', 'couchdb', 'firebase'
    ],
    
    # Cloud & DevOps
    'cloud_devops': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
        'ansible', 'git', 'github', 'gitlab', 'bitbucket', 'ci/cd', 'circleci',
        'travis ci', 'nginx', 'apache', 'linux', 'unix'
    ],
    
    # Mobile Development
    'mobile': [
        'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic',
        'swift', 'kotlin', 'objective-c'
    ],
    
    # Data Science & ML
    'data_science': [
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
        'scikit-learn', 'pandas', 'numpy', 'data analysis', 'data visualization',
        'tableau', 'power bi', 'jupyter', 'nlp', 'computer vision', 'opencv',
        'spark', 'hadoop', 'big data', 'statistics', 'probability'
    ],
    
    # Testing
    'testing': [
        'selenium', 'junit', 'pytest', 'jest', 'mocha', 'cypress', 'testing',
        'unit testing', 'integration testing', 'test automation', 'qa'
    ],
    
    # Soft Skills
    'soft_skills': [
        'communication', 'teamwork', 'leadership', 'problem solving',
        'critical thinking', 'time management', 'project management',
        'agile', 'scrum', 'collaboration', 'analytical', 'creative'
    ],
    
    # Other Technologies
    'other': [
        'rest api', 'graphql', 'websocket', 'microservices', 'api', 'json',
        'xml', 'html', 'css', 'sass', 'less', 'webpack', 'babel', 'redux',
        'oauth', 'jwt', 'security', 'encryption', 'blockchain', 'iot'
    ]
}

# Flatten all skills into one list
ALL_SKILLS = []
for category_skills in SKILLS_DATABASE.values():
    ALL_SKILLS.extend(category_skills)

# Remove duplicates and sort
ALL_SKILLS = sorted(list(set(ALL_SKILLS)))

# Skill variations (e.g., "react.js" should match "react")
SKILL_VARIATIONS = {
    'react.js': 'react',
    'reactjs': 'react',
    'node.js': 'nodejs',
    'vue.js': 'vue',
    'vuejs': 'vue',
    'angular.js': 'angular',
    'angularjs': 'angular',
    'next.js': 'nextjs',
    'nuxt.js': 'nuxt',
    'express.js': 'express',
    'c++': 'cpp',
    'c#': 'csharp',
    '.net': 'asp.net',
    'ml': 'machine learning',
    'ai': 'artificial intelligence',
    'dl': 'deep learning',
    'tf': 'tensorflow',
    'k8s': 'kubernetes',
}