import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Database, BarChart3, Users, ArrowRight, Check } from 'lucide-react';
import { mockData } from '../mock';

const Services = () => {
  const { services } = mockData;

  const getIcon = (iconName) => {
    const icons = {
      Database: Database,
      BarChart3: BarChart3,
      Users: Users
    };
    const Icon = icons[iconName];
    return Icon ? <Icon className="h-8 w-8" /> : <Database className="h-8 w-8" />;
  };

  return (
    <section id="services" className="py-20 bg-white">
      <div className="container mx-auto px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge variant="outline" className="mb-4 text-blue-600 border-blue-600">
            Our Services
          </Badge>
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Comprehensive Database Solutions
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            From simple database creation to complex data analysis, we provide tailored solutions 
            that transform how your business manages and leverages data.
          </p>
        </div>

        {/* Services Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {services.map((service, index) => (
            <Card key={service.id} className="relative overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 group">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-600 to-cyan-600"></div>
              
              <CardHeader className="pb-4">
                <div className="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center text-blue-600 mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors duration-300">
                  {getIcon(service.icon)}
                </div>
                <CardTitle className="text-xl font-bold text-gray-900 mb-2">
                  {service.title}
                </CardTitle>
                <CardDescription className="text-gray-600">
                  {service.description}
                </CardDescription>
              </CardHeader>

              <CardContent className="pt-0">
                {/* Features */}
                <ul className="space-y-2 mb-6">
                  {service.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center text-sm text-gray-600">
                      <Check className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>

                {/* Pricing (if available) */}
                {service.pricing && (
                  <div className="border-t pt-4 mb-6">
                    <p className="text-sm font-medium text-gray-900 mb-2">Starting from:</p>
                    <div className="space-y-1">
                      {service.pricing.basic && (
                        <p className="text-sm text-gray-600">Basic: {service.pricing.basic}</p>
                      )}
                      {service.pricing.hourly && (
                        <p className="text-sm text-gray-600">Hourly: {service.pricing.hourly}</p>
                      )}
                    </div>
                  </div>
                )}

                <Button variant="outline" className="w-full group-hover:bg-blue-600 group-hover:text-white group-hover:border-blue-600 transition-colors duration-300">
                  Learn More
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* CTA Section */}
        <div className="text-center bg-gray-50 rounded-2xl p-8 lg:p-12">
          <h3 className="text-2xl lg:text-3xl font-bold text-gray-900 mb-4">
            Ready to Transform Your Data Management?
          </h3>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Get a free consultation to discuss your specific needs and discover how we can help 
            streamline your business operations.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8">
              Schedule Free Consultation
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button variant="outline" size="lg" className="border-blue-600 text-blue-600 hover:bg-blue-50 px-8">
              View Case Studies
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Services;