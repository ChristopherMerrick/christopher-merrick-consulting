import React from 'react';
import { Button } from './ui/button';
import { ArrowRight, MapPin, Phone } from 'lucide-react';
import { mockData } from '../mock';

const Hero = () => {
  const { hero, contact } = mockData;

  return (
    <section className="relative min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23e2e8f0" fill-opacity="0.3"%3E%3Ccircle cx="7" cy="7" r="1"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-40"></div>
      
      <div className="container mx-auto px-6 lg:px-8 relative z-10">
        <div className="flex flex-col lg:flex-row items-center justify-between min-h-screen py-20">
          {/* Content */}
          <div className="lg:w-1/2 text-center lg:text-left mb-12 lg:mb-0">
            <div className="flex items-center justify-center lg:justify-start mb-6">
              <MapPin className="h-5 w-5 text-blue-600 mr-2" />
              <span className="text-blue-600 font-medium">Sheffield, UK • Serving Nationwide</span>
            </div>
            
            <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Expert <span className="text-blue-600">Database Solutions</span> for UK Businesses
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 leading-relaxed max-w-2xl">
              Transform your business operations with bespoke Microsoft Access databases. 
              Professional data consulting services that turn complexity into competitive advantage.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start mb-8">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg">
                Get Free Consultation
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              
              <Button variant="outline" size="lg" className="border-blue-600 text-blue-600 hover:bg-blue-50 px-8 py-3 text-lg">
                <Phone className="mr-2 h-5 w-5" />
                {contact.phone}
              </Button>
            </div>
            
            {/* Trust Indicators */}
            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-6 text-sm text-gray-500">
              <div className="flex items-center">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                Available Nationwide
              </div>
              <div className="flex items-center">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                GDPR Compliant
              </div>
              <div className="flex items-center">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                Free Consultation
              </div>
            </div>
          </div>
          
          {/* Image */}
          <div className="lg:w-1/2 flex justify-center lg:justify-end">
            <div className="relative">
              <div className="absolute -inset-4 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-2xl blur-2xl opacity-20"></div>
              <img
                src={hero.image}
                alt="Database consulting services"
                className="relative rounded-2xl shadow-2xl w-full max-w-lg h-96 object-cover"
              />
              
              {/* Floating Card */}
              <div className="absolute -bottom-6 -left-6 bg-white rounded-xl shadow-lg p-4 border">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold text-lg">CM</span>
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">Christopher Merrick</p>
                    <p className="text-sm text-gray-500">Data Engineer</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;