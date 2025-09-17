import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { AlertCircle, ArrowRight, CheckCircle } from 'lucide-react';
import { mockData } from '../mock';

const ProblemIdentification = () => {
  const { painPoints } = mockData;

  return (
    <section className="py-20 bg-gradient-to-br from-red-50 to-orange-50">
      <div className="container mx-auto px-6 lg:px-8">
        <div className="flex flex-col lg:flex-row items-center gap-12">
          {/* Image */}
          <div className="lg:w-1/2">
            <div className="relative">
              <img
                src="https://images.unsplash.com/photo-1551434678-e076c223a692?w=600&h=500&fit=crop&crop=entropy"
                alt="Business person overwhelmed with spreadsheets"
                className="rounded-2xl shadow-2xl w-full h-96 object-cover"
              />
              <div className="absolute -top-4 -right-4 bg-red-500 text-white rounded-full p-3 shadow-lg">
                <AlertCircle className="h-8 w-8" />
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="lg:w-1/2">
            <Badge variant="outline" className="mb-4 text-red-600 border-red-600">
              Do You Need Help?
            </Badge>
            
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-6">
              Are These Problems <span className="text-red-600">Holding Your Business Back?</span>
            </h2>
            
            <p className="text-lg text-gray-600 mb-8">
              If you're experiencing any of these common business challenges, you're not alone. 
              Many UK businesses struggle with inefficient data management.
            </p>

            {/* Pain Points List */}
            <div className="space-y-3 mb-8">
              {painPoints.map((point, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <AlertCircle className="h-5 w-5 text-red-500 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{point}</span>
                </div>
              ))}
            </div>

            {/* Solution Card */}
            <Card className="border-green-200 bg-green-50">
              <CardContent className="p-6">
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-green-600 mt-1" />
                  <div>
                    <h3 className="font-semibold text-green-900 mb-2">
                      The Good News: These Problems Are Solvable
                    </h3>
                    <p className="text-green-700 text-sm mb-4">
                      With the right database solution, you can eliminate these pain points and 
                      transform your business operations for improved efficiency and growth.
                    </p>
                    <Button className="bg-green-600 hover:bg-green-700 text-white">
                      See How We Can Help
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProblemIdentification;