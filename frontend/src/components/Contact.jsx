import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Phone, Mail, MapPin, Clock, Send, CheckCircle, AlertCircle } from 'lucide-react';
import { mockData } from '../mock';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Contact = () => {
  const { contact, consultations } = mockData;
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    consultationType: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      const response = await axios.post(`${API}/contact`, formData);
      
      if (response.data.success) {
        setIsSubmitted(true);
        // Reset form
        setFormData({
          name: '',
          email: '',
          phone: '',
          company: '',
          consultationType: '',
          message: ''
        });
        
        // Reset success message after 5 seconds
        setTimeout(() => setIsSubmitted(false), 5000);
      }
    } catch (error) {
      console.error('Error submitting contact form:', error);
      setError('There was an error sending your message. Please try again or contact us directly.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    // Clear error when user starts typing
    if (error) setError('');
  };

  return (
    <section id="contact" className="py-20 bg-gray-50">
      <div className="container mx-auto px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge variant="outline" className="mb-4 text-blue-600 border-blue-600">
            Get In Touch
          </Badge>
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-6">
            Ready to Transform Your <span className="text-blue-600">Business Data?</span>
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Let's discuss your database needs. Start with a free consultation to explore 
            how we can help streamline your operations.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Contact Information */}
          <div className="lg:col-span-1">
            <Card className="border-0 shadow-lg mb-8">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-gray-900">
                  Contact Information
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <Phone className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Phone</p>
                    <p className="text-gray-600">{contact.phone}</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <Mail className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Email</p>
                    <p className="text-gray-600">{contact.email}</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <MapPin className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Location</p>
                    <p className="text-gray-600">{contact.address}</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <Clock className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Hours</p>
                    <p className="text-gray-600">{contact.hours}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Consultation Types */}
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-gray-900">
                  Consultation Options
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {consultations.map((consultation) => (
                  <div key={consultation.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors duration-200">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-semibold text-gray-900">{consultation.name}</h4>
                      <Badge variant={consultation.price === 'FREE' ? 'success' : 'secondary'}>
                        {consultation.price}
                      </Badge>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{consultation.description}</p>
                    <p className="text-xs text-blue-600">{consultation.duration}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Contact Form */}
          <div className="lg:col-span-2">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-gray-900">
                  Send us a Message
                </CardTitle>
              </CardHeader>
              <CardContent>
                {isSubmitted ? (
                  <div className="text-center py-12">
                    <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Message Sent Successfully!</h3>
                    <p className="text-gray-600">
                      Thank you for your inquiry. We'll get back to you within 24 hours.
                    </p>
                  </div>
                ) : (
                  <form onSubmit={handleSubmit} className="space-y-6">
                    {error && (
                      <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center">
                        <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
                        <p className="text-red-700">{error}</p>
                      </div>
                    )}

                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Full Name *
                        </label>
                        <Input
                          type="text"
                          required
                          value={formData.name}
                          onChange={(e) => handleChange('name', e.target.value)}
                          placeholder="Your full name"
                          className="w-full"
                          disabled={isSubmitting}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Email Address *
                        </label>
                        <Input
                          type="email"
                          required
                          value={formData.email}
                          onChange={(e) => handleChange('email', e.target.value)}
                          placeholder="your@email.com"
                          className="w-full"
                          disabled={isSubmitting}
                        />
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Phone Number
                        </label>
                        <Input
                          type="tel"
                          value={formData.phone}
                          onChange={(e) => handleChange('phone', e.target.value)}
                          placeholder="+44 xxx xxx xxxx"
                          className="w-full"
                          disabled={isSubmitting}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Company Name
                        </label>
                        <Input
                          type="text"
                          value={formData.company}
                          onChange={(e) => handleChange('company', e.target.value)}
                          placeholder="Your company name"
                          className="w-full"
                          disabled={isSubmitting}
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Consultation Type
                      </label>
                      <Select onValueChange={(value) => handleChange('consultationType', value)} disabled={isSubmitting}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select consultation type" />
                        </SelectTrigger>
                        <SelectContent>
                          {consultations.map((consultation) => (
                            <SelectItem key={consultation.id} value={consultation.name.toLowerCase()}>
                              {consultation.name} - {consultation.price}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Project Details *
                      </label>
                      <Textarea
                        required
                        value={formData.message}
                        onChange={(e) => handleChange('message', e.target.value)}
                        placeholder="Please describe your database needs, current challenges, and what you hope to achieve..."
                        rows={5}
                        className="w-full"
                        disabled={isSubmitting}
                      />
                    </div>

                    <div className="text-sm text-gray-600 bg-blue-50 p-4 rounded-lg">
                      <p className="mb-2">
                        <strong>GDPR Notice:</strong> By submitting this form, you consent to us storing and processing your personal data for the purpose of responding to your inquiry.
                      </p>
                      <p>We will not share your information with third parties and you can request deletion at any time.</p>
                    </div>

                    <Button 
                      type="submit" 
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3"
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? (
                        <>
                          <div className="animate-spin mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                          Sending...
                        </>
                      ) : (
                        <>
                          <Send className="mr-2 h-4 w-4" />
                          Send Message
                        </>
                      )}
                    </Button>
                  </form>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;