import React, { useState, useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Star, Quote } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Testimonials = () => {
  const [testimonials, setTestimonials] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTestimonials();
  }, []);

  const fetchTestimonials = async () => {
    try {
      const response = await axios.get(`${API}/testimonials`);
      setTestimonials(response.data);
    } catch (error) {
      console.error('Error fetching testimonials:', error);
      // Fallback to mock data if API fails
      const { mockData } = await import('../mock');
      setTestimonials(mockData.testimonials);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <section className="py-20 bg-white">
        <div className="container mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-32 mx-auto mb-4"></div>
              <div className="h-10 bg-gray-200 rounded w-96 mx-auto mb-6"></div>
              <div className="h-6 bg-gray-200 rounded w-2/3 mx-auto"></div>
            </div>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map((item) => (
              <Card key={item} className="animate-pulse">
                <CardContent className="p-6">
                  <div className="flex items-center mb-4">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <div key={star} className="h-4 w-4 bg-gray-200 rounded mr-1"></div>
                    ))}
                  </div>
                  <div className="space-y-2 mb-6">
                    <div className="h-4 bg-gray-200 rounded w-full"></div>
                    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                    <div className="h-4 bg-gray-200 rounded w-4/6"></div>
                  </div>
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-gray-200 rounded-full mr-4"></div>
                    <div>
                      <div className="h-4 bg-gray-200 rounded w-24 mb-1"></div>
                      <div className="h-3 bg-gray-200 rounded w-16"></div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge variant="outline" className="mb-4 text-blue-600 border-blue-600">
            Client Testimonials
          </Badge>
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-6">
            What Our <span className="text-blue-600">Clients Say</span>
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Don't just take our word for it. Here's what business owners across the UK 
            are saying about our database solutions.
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial) => (
            <Card key={testimonial.id || testimonial._id} className="relative border-0 shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden">
              {/* Quote Icon */}
              <div className="absolute top-4 right-4 opacity-10">
                <Quote className="h-12 w-12 text-blue-600" />
              </div>
              
              <CardContent className="p-6">
                {/* Stars */}
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                  ))}
                </div>

                {/* Testimonial Text */}
                <blockquote className="text-gray-700 mb-6 italic leading-relaxed">
                  "{testimonial.text}"
                </blockquote>

                {/* Author Info */}
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                    <span className="text-blue-600 font-semibold text-lg">
                      {testimonial.name.split(' ').map(n => n[0]).join('')}
                    </span>
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">{testimonial.name}</p>
                    <p className="text-sm text-gray-600">{testimonial.company}</p>
                    <p className="text-xs text-blue-600">{testimonial.location}</p>
                  </div>
                </div>
              </CardContent>

              {/* Accent Border */}
              <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-blue-600 to-cyan-600"></div>
            </Card>
          ))}
        </div>

        {/* CTA Section */}
        <div className="text-center mt-16">
          <Card className="bg-gray-50 border-0">
            <CardContent className="p-8 lg:p-12">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Ready to Join Our Satisfied Clients?
              </h3>
              <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
                Experience the same transformation these businesses achieved. 
                Start with a free consultation to discuss your needs.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-md font-medium transition-colors duration-200">
                  Get Your Free Quote
                </button>
                <button className="border border-blue-600 text-blue-600 hover:bg-blue-50 px-8 py-3 rounded-md font-medium transition-colors duration-200">
                  View More Reviews
                </button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;