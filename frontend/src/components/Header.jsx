import React, { useState } from 'react';
import { Button } from './ui/button';
import { Menu, X, Phone, Mail } from 'lucide-react';
import { mockData } from '../mock';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { contact } = mockData;

  const navigation = [
    { name: 'Home', href: '#home' },
    { name: 'Services', href: '#services' },
    { name: 'About', href: '#about' },
    { name: 'Pricing', href: '#pricing' },
    { name: 'Blog', href: '#blog' },
    { name: 'Contact', href: '#contact' }
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-200">
      {/* Top Bar */}
      <div className="bg-blue-600 text-white text-sm py-2">
        <div className="container mx-auto px-6 lg:px-8 flex justify-between items-center">
          <div className="flex items-center space-x-6">
            <div className="flex items-center">
              <Phone className="h-4 w-4 mr-2" />
              <span>{contact.phone}</span>
            </div>
            <div className="flex items-center">
              <Mail className="h-4 w-4 mr-2" />
              <span>{contact.email}</span>
            </div>
          </div>
          <div className="hidden md:block">
            <span>Sheffield • Serving UK Nationwide</span>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="container mx-auto px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">CM</span>
            </div>
            <div>
              <h1 className="font-bold text-xl text-gray-900">Christopher Merrick</h1>
              <p className="text-sm text-gray-500">Database Consulting</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-8">
            {navigation.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors duration-200"
              >
                {item.name}
              </a>
            ))}
          </div>

          {/* CTA Button */}
          <div className="hidden lg:block">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white">
              Free Consultation
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="lg:hidden p-2"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? (
              <X className="h-6 w-6 text-gray-700" />
            ) : (
              <Menu className="h-6 w-6 text-gray-700" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="lg:hidden mt-4 py-4 border-t border-gray-200">
            <div className="flex flex-col space-y-3">
              {navigation.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-gray-700 hover:text-blue-600 font-medium py-2 transition-colors duration-200"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </a>
              ))}
              <Button className="bg-blue-600 hover:bg-blue-700 text-white w-full mt-4">
                Free Consultation
              </Button>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;