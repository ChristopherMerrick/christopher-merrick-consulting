// Mock data for Christopher Merrick Database Consulting Website

export const mockData = {
  // Hero Section
  hero: {
    title: "Expert Access Database Solutions for UK Businesses",
    subtitle: "Transform your business operations with bespoke Microsoft Access databases. Sheffield-based consultant serving nationwide.",
    cta: "Get Free Consultation",
    image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop&crop=entropy"
  },

  // Services
  services: [
    {
      id: 1,
      title: "Custom Access Databases",
      description: "Bespoke Microsoft Access databases designed to streamline your operations and unlock your organisation's potential.",
      icon: "Database",
      features: ["Custom forms and reports", "Data relationships", "User-friendly interfaces", "Scalable solutions"],
      pricing: {
        basic: "£750 - £2,000",
        intermediate: "£2,000 - £7,500", 
        advanced: "£7,500+"
      }
    },
    {
      id: 2,
      title: "Data Analysis & Insights",
      description: "Transform raw data into actionable insights that drive informed business decisions and competitive advantage.",
      icon: "BarChart3",
      features: ["Data visualization", "Performance metrics", "Trend analysis", "Custom reporting"]
    },
    {
      id: 3,
      title: "Database Consulting",
      description: "Expert guidance on data strategy, optimization, and system integration. Available from 1-hour sessions to full-day reviews.",
      icon: "Users",
      features: ["System optimization", "Data strategy", "Process improvement", "Staff training"],
      pricing: {
        hourly: "£80/hour",
        halfDay: "£300",
        fullDay: "£550"
      }
    }
  ],

  // Problems/Pain Points
  painPoints: [
    "Multiple spreadsheets that don't talk to each other",
    "Software becoming too expensive or inflexible",
    "Old databases that no longer work properly",
    "Too much time spent on manual admin tasks",
    "Lack of visibility into staff activities",
    "Feeling overwhelmed by data management",
    "Competitors seem to operate more efficiently"
  ],

  // About
  about: {
    name: "Christopher Merrick",
    title: "Data Engineer & Access Database Specialist",
    location: "Sheffield, UK",
    description: "With years of experience creating bespoke Access databases and providing data analysis, I help UK businesses turn data into strategic advantage. Based in Sheffield but serving clients nationwide.",
    expertise: [
      "Microsoft Access Development",
      "Database Design & Optimization",
      "Data Analysis & Reporting",
      "System Integration",
      "Process Automation"
    ]
  },

  // Testimonials
  testimonials: [
    {
      id: 1,
      name: "Sarah Johnson",
      company: "Johnson Manufacturing Ltd",
      location: "Manchester",
      text: "Christopher created an amazing system to track all our inventory and orders. It's saved us countless hours and improved our accuracy dramatically.",
      rating: 5
    },
    {
      id: 2,
      name: "David Wright",
      company: "Wright Consulting",
      location: "Birmingham",
      text: "The database solution Christopher built has transformed how we manage client data. Professional service and excellent results.",
      rating: 5
    },
    {
      id: 3,
      name: "Emma Thompson",
      company: "Thompson Logistics",
      location: "Leeds",
      text: "Highly recommend Christopher's services. He understood our complex requirements and delivered exactly what we needed.",
      rating: 5
    }
  ],

  // Blog Posts (for SEO)
  blogPosts: [
    {
      id: 1,
      title: "5 Signs Your Business Needs a Custom Database Solution",
      excerpt: "Discover when it's time to move beyond spreadsheets and invest in a proper database system.",
      date: "2024-01-15",
      category: "Database Strategy",
      readTime: "5 min read"
    },
    {
      id: 2,
      title: "Microsoft Access vs. Excel: Which is Right for Your Business?",
      excerpt: "Understanding the key differences and when to make the switch from Excel to Access.",
      date: "2024-01-10",
      category: "Technology Comparison",
      readTime: "7 min read"
    },
    {
      id: 3,
      title: "GDPR Compliance for UK Businesses: Database Best Practices",
      excerpt: "Essential guidelines for ensuring your database systems meet UK data protection requirements.",
      date: "2024-01-05",
      category: "Compliance",
      readTime: "6 min read"
    }
  ],

  // Contact Information
  contact: {
    phone: "+44 114 123 4567",
    email: "hello@christophermerrick.co.uk",
    address: "Sheffield, South Yorkshire, UK",
    hours: "Monday - Friday: 9:00 AM - 6:00 PM"
  },

  // Consultation Types
  consultations: [
    {
      id: 1,
      name: "Free Quote Consultation",
      duration: "30 minutes",
      price: "FREE",
      description: "Get a no-obligation quote for your database project",
      features: ["Project scope discussion", "Initial requirements review", "Cost estimation"]
    },
    {
      id: 2,
      name: "Strategy Consultation",
      duration: "1 hour",
      price: "£80",
      description: "In-depth consultation on your data strategy and needs",
      features: ["Current system review", "Improvement recommendations", "Next steps planning"]
    },
    {
      id: 3,
      name: "Comprehensive Review",
      duration: "Half day",
      price: "£300",
      description: "Detailed on-site or remote review of your data systems",
      features: ["Full system audit", "Detailed report", "Implementation roadmap"]
    }
  ]
};

// CMS Mock Data
export const cmsData = {
  pages: [
    { id: 1, title: "Home", status: "published", lastModified: "2024-01-15" },
    { id: 2, title: "Services", status: "published", lastModified: "2024-01-14" },
    { id: 3, title: "About", status: "published", lastModified: "2024-01-13" },
    { id: 4, title: "Contact", status: "published", lastModified: "2024-01-12" }
  ],
  
  blogStats: {
    totalPosts: 3,
    publishedPosts: 3,
    draftPosts: 0,
    totalViews: 1247
  },

  recentContacts: [
    { id: 1, name: "John Smith", email: "john@example.com", date: "2024-01-15", type: "Quote Request" },
    { id: 2, name: "Lisa Brown", email: "lisa@company.com", date: "2024-01-14", type: "Consultation" }
  ]
};