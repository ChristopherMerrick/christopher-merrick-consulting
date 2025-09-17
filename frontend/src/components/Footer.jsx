import React from 'react';
import { MapPin, Phone, Mail, Facebook, Twitter, Linkedin } from 'lucide-react';
import { mockData } from '../mock';

const Footer = () => {
  const { contact } = mockData;
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    services: [
      { name: 'Access Databases', href: '#services' },
      { name: 'Data Analysis', href: '#services' },
      { name: 'Database Consulting', href: '#services' },
      { name: 'System Integration', href: '#services' }
    ],
    company: [
      { name: 'About', href: '#about' },
      { name: 'Case Studies', href: '#testimonials' },
      { name: 'Blog', href: '#blog' },
      { name: 'Contact', href: '#contact' }
    ],
    legal: [
      { name: 'Privacy Policy', href: '/privacy' },
      { name: 'Terms of Service', href: '/terms' },
      { name: 'GDPR Compliance', href: '/gdpr' },
      { name: 'Cookie Policy', href: '/cookies' }
    ]
  };

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main Footer */}
      <div className="container mx-auto px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="lg:col-span-1">
            <div className="flex items-center space-x-2 mb-6">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">CM</span>
              </div>
              <div>
                <h3 className="font-bold text-xl">Christopher Merrick</h3>
                <p className="text-sm text-gray-400">Database Consulting</p>
              </div>
            </div>
            
            <p className="text-gray-400 mb-6 leading-relaxed">
              Expert Access database solutions for UK businesses. Transform your data management 
              and unlock your business potential with professional consulting services.
            </p>

            {/* Contact Info */}
            <div className="space-y-3">
              <div className="flex items-center text-gray-400">
                <MapPin className="h-4 w-4 mr-2 flex-shrink-0" />
                <span className="text-sm">{contact.address}</span>
              </div>
              <div className="flex items-center text-gray-400">
                <Phone className="h-4 w-4 mr-2 flex-shrink-0" />
                <span className="text-sm">{contact.phone}</span>
              </div>
              <div className="flex items-center text-gray-400">
                <Mail className="h-4 w-4 mr-2 flex-shrink-0" />
                <span className="text-sm">{contact.email}</span>
              </div>
            </div>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-semibold text-lg mb-6">Services</h4>
            <ul className="space-y-3">
              {footerLinks.services.map((link, index) => (
                <li key={index}>
                  <a 
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors duration-200 text-sm"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="font-semibold text-lg mb-6">Company</h4>
            <ul className="space-y-3">
              {footerLinks.company.map((link, index) => (
                <li key={index}>
                  <a 
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors duration-200 text-sm"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal & Newsletter */}
          <div>
            <h4 className="font-semibold text-lg mb-6">Legal & Updates</h4>
            <ul className="space-y-3 mb-8">
              {footerLinks.legal.map((link, index) => (
                <li key={index}>
                  <a 
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors duration-200 text-sm"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>

            {/* Newsletter Signup */}
            <div>
              <h5 className="font-medium mb-3">Stay Updated</h5>
              <p className="text-gray-400 text-sm mb-4">
                Get database tips and insights delivered to your inbox.
              </p>
              <div className="flex space-x-2">
                <input
                  type="email"
                  placeholder="Your email"
                  className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-sm focus:outline-none focus:border-blue-600"
                />
                <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  Subscribe
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800">
        <div className="container mx-auto px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-gray-400 text-sm mb-4 md:mb-0">
              © {currentYear} Christopher Merrick Database Consulting. All rights reserved.
            </div>
            
            {/* Social Links */}
            <div className="flex space-x-4">
              <a 
                href="#" 
                className="text-gray-400 hover:text-white transition-colors duration-200"
                aria-label="Facebook"
              >
                <Facebook className="h-5 w-5" />
              </a>
              <a 
                href="#" 
                className="text-gray-400 hover:text-white transition-colors duration-200"
                aria-label="Twitter"
              >
                <Twitter className="h-5 w-5" />
              </a>
              <a 
                href="#" 
                className="text-gray-400 hover:text-white transition-colors duration-200"
                aria-label="LinkedIn"
              >
                <Linkedin className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;