import React from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { MapPin, Award, Users, Clock, ArrowRight } from 'lucide-react';
import { mockData } from '../mock';

const About = () => {
  const { about } = mockData;

  const stats = [
    { icon: Users, label: "Happy Clients", value: "50+" },
    { icon: Award, label: "Years Experience", value: "10+" },
    { icon: Clock, label: "Projects Completed", value: "100+" }
  ];

  return (
    <section id="about" className="py-20 bg-gray-50">
      <div className="container mx-auto px-6 lg:px-8">
        <div className="flex flex-col lg:flex-row items-center gap-12">
          {/* Content */}
          <div className="lg:w-1/2">
            <Badge variant="outline" className="mb-4 text-blue-600 border-blue-600">
              About Christopher
            </Badge>
            
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-6">
              Your Trusted <span className="text-blue-600">Database Partner</span> in the UK
            </h2>
            
            <p className="text-lg text-gray-600 mb-6 leading-relaxed">
              {about.description}
            </p>

            <div className="flex items-center mb-8">
              <MapPin className="h-5 w-5 text-blue-600 mr-2" />
              <span className="text-gray-700 font-medium">{about.location} • Nationwide Service</span>
            </div>

            {/* Expertise */}
            <div className="mb-8">
              <h3 className="font-semibold text-gray-900 mb-4">Core Expertise:</h3>
              <div className="flex flex-wrap gap-2">
                {about.expertise.map((skill, index) => (
                  <Badge key={index} variant="secondary" className="bg-blue-100 text-blue-800">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>

            <Button className="bg-blue-600 hover:bg-blue-700 text-white">
              Schedule a Meeting
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>

          {/* Image and Stats */}
          <div className="lg:w-1/2">
            <div className="relative">
              {/* Main Image */}
              <div className="relative">
                <img
                  src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=500&fit=crop&crop=face"
                  alt="Christopher Merrick - Database Consultant"
                  className="rounded-2xl shadow-2xl w-full max-w-md mx-auto h-96 object-cover"
                />
                
                {/* Professional Badge */}
                <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 bg-white rounded-xl shadow-lg p-4 border">
                  <div className="text-center">
                    <p className="font-bold text-gray-900">{about.name}</p>
                    <p className="text-sm text-blue-600">{about.title}</p>
                  </div>
                </div>
              </div>

              {/* Stats Cards */}
              <div className="grid grid-cols-3 gap-4 mt-12">
                {stats.map((stat, index) => (
                  <Card key={index} className="border-0 shadow-md hover:shadow-lg transition-shadow duration-300">
                    <CardContent className="p-4 text-center">
                      <stat.icon className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                      <p className="font-bold text-2xl text-gray-900">{stat.value}</p>
                      <p className="text-sm text-gray-600">{stat.label}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Values Section */}
        <div className="mt-20">
          <div className="text-center mb-12">
            <h3 className="text-2xl lg:text-3xl font-bold text-gray-900 mb-4">
              Why Choose Christopher Merrick?
            </h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Combining technical expertise with business understanding to deliver solutions that work.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Award className="h-6 w-6 text-blue-600" />
                </div>
                <h4 className="font-semibold text-gray-900 mb-2">Expert Knowledge</h4>
                <p className="text-gray-600 text-sm">
                  Years of experience with Microsoft Access and database optimization for UK businesses.
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="h-6 w-6 text-blue-600" />
                </div>
                <h4 className="font-semibold text-gray-900 mb-2">Client-Focused</h4>
                <p className="text-gray-600 text-sm">
                  Tailored solutions that fit your specific business needs and growth objectives.
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Clock className="h-6 w-6 text-blue-600" />
                </div>
                <h4 className="font-semibold text-gray-900 mb-2">Reliable Service</h4>
                <p className="text-gray-600 text-sm">
                  Prompt communication, on-time delivery, and ongoing support for peace of mind.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;