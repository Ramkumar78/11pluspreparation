import React, { useState } from 'react';
import { Calculator, BookOpen, Brain, Grid, TrendingUp } from 'lucide-react';

const mockSkills = {
  Mathematics: [
    { name: 'Number & Place Value', mastery: 80 },
    { name: 'Calculation', mastery: 70 },
    { name: 'Fractions, Decimals, Percentages', mastery: 40 },
    { name: 'Ratio & Proportion', mastery: 60 },
    { name: 'Algebra', mastery: 50 },
    { name: 'Measurement', mastery: 90 },
    { name: 'Geometry', mastery: 30 },
    { name: 'Statistics & Data', mastery: 85 },
  ],
  English: [
    { name: 'Reading Comprehension', mastery: 75 },
    { name: 'Vocabulary', mastery: 65 },
    { name: 'Grammar & Punctuation (SPaG)', mastery: 80 },
  ],
  'Verbal Reasoning': [
    { name: 'Constructing Words', mastery: 55 },
    { name: 'Understanding Words', mastery: 60 },
    { name: 'Codes & Sequences', mastery: 70 },
    { name: 'Logic', mastery: 45 },
  ],
  'Non-Verbal Reasoning': [
    { name: 'Patterns & Series', mastery: 20 },
    { name: 'Spatial Awareness', mastery: 10 },
  ],
};

const domainIcons = {
  Mathematics: Calculator,
  English: BookOpen,
  'Verbal Reasoning': Brain,
  'Non-Verbal Reasoning': Grid,
};

export default function SkillMatrix() {
  const [activeTab, setActiveTab] = useState('Mathematics');

  const getProgressColor = (value) => {
    if (value >= 80) return 'bg-green-500';
    if (value >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <TrendingUp className="text-indigo-600" /> Skills Mastery Matrix
          </h2>
          <p className="text-gray-500 text-sm mt-1">
            Track your progress across all 11+ curriculum domains.
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 mb-6 border-b border-gray-100 pb-4">
        {Object.keys(mockSkills).map((domain) => {
          const Icon = domainIcons[domain];
          const isActive = activeTab === domain;
          return (
            <button
              key={domain}
              onClick={() => setActiveTab(domain)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold transition-all
                ${isActive
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'}`}
            >
              <Icon size={16} />
              <span className="hidden sm:inline">{domain}</span>
              <span className="sm:hidden">{domain.split(' ')[0]}</span>
            </button>
          );
        })}
      </div>

      {/* Content */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
        {mockSkills[activeTab].map((skill, index) => (
          <div key={index} className="flex flex-col gap-1 mb-2 group">
            <div className="flex justify-between items-center text-sm mb-1">
              <span className="font-medium text-gray-700 group-hover:text-indigo-700 transition-colors">
                {skill.name}
              </span>
              <span className={`font-bold ${
                skill.mastery >= 80 ? 'text-green-600' :
                skill.mastery >= 50 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {skill.mastery}%
              </span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
              <div
                className={`h-2.5 rounded-full transition-all duration-1000 ${getProgressColor(skill.mastery)}`}
                style={{ width: `${skill.mastery}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
