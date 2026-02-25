import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { User, Plus, Trash2, ArrowRight, Trophy } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

export default function ProfileSelection({ onSelectProfile }) {
    const [profiles, setProfiles] = useState([]);
    const [newName, setNewName] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchProfiles();
    }, []);

    const fetchProfiles = async () => {
        try {
            const res = await axios.get(`${API_URL}/profiles`);
            setProfiles(res.data);
        } catch (err) {
            console.error("Failed to fetch profiles", err);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        if (!newName.trim()) return;

        setLoading(true);
        setError("");
        try {
            const res = await axios.post(`${API_URL}/profiles`, { name: newName });
            setProfiles([...profiles, res.data]);
            setNewName("");
            // Auto-select the new profile? Or just let them click it.
        } catch (err) {
            setError(err.response?.data?.error || "Failed to create profile");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id, name, e) => {
        e.stopPropagation(); // Prevent selection when clicking delete
        if (!window.confirm(`Are you sure you want to delete "${name}"? This will ERASE all progress!`)) return;

        try {
            await axios.delete(`${API_URL}/profiles/${id}`);
            setProfiles(profiles.filter(p => p.id !== id));
        } catch (err) {
            console.error("Failed to delete profile", err);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex flex-col items-center justify-center p-4">
            <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full relative overflow-hidden">

                {/* Header */}
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-black text-indigo-900 mb-2">Who is playing?</h1>
                    <p className="text-gray-500 font-medium">Select your profile to load progress</p>
                </div>

                {/* Profile List */}
                <div className="space-y-4 mb-8 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                    {profiles.map(profile => (
                        <div
                            key={profile.id}
                            onClick={() => onSelectProfile(profile.id)}
                            className="group flex items-center justify-between p-4 bg-gray-50 hover:bg-indigo-50 border-2 border-gray-100 hover:border-indigo-300 rounded-xl cursor-pointer transition-all transform hover:-translate-y-1 hover:shadow-md"
                        >
                            <div className="flex items-center gap-4">
                                <div className="bg-indigo-100 p-3 rounded-full text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                                    <User className="w-6 h-6" />
                                </div>
                                <div>
                                    <h3 className="font-bold text-lg text-gray-800 group-hover:text-indigo-900">{profile.name}</h3>
                                    <div className="flex items-center gap-2 text-sm text-gray-500">
                                        <span className="flex items-center gap-1 text-yellow-600 font-bold"><Trophy className="w-3 h-3" /> Lvl {profile.level}</span>
                                        <span>•</span>
                                        <span>{profile.score} pts</span>
                                    </div>
                                </div>
                            </div>

                            <button
                                onClick={(e) => handleDelete(profile.id, profile.name, e)}
                                className="p-2 text-gray-300 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors opacity-0 group-hover:opacity-100"
                                title="Clear Progress"
                            >
                                <Trash2 className="w-5 h-5" />
                            </button>
                        </div>
                    ))}

                    {profiles.length === 0 && (
                        <div className="text-center py-8 text-gray-400 italic">
                            No profiles yet. Create one below!
                        </div>
                    )}
                </div>

                {/* Create Form */}
                <form onSubmit={handleCreate} className="relative">
                    <input
                        type="text"
                        placeholder="Enter your name..."
                        value={newName}
                        onChange={(e) => setNewName(e.target.value)}
                        className="w-full pl-5 pr-14 py-4 rounded-xl border-2 border-gray-200 focus:border-indigo-500 focus:outline-none font-bold text-gray-700 bg-gray-50 focus:bg-white transition-all uppercase placeholder-gray-400"
                        maxLength={12}
                    />
                    <button
                        type="submit"
                        disabled={!newName.trim() || loading}
                        className="absolute right-2 top-2 bottom-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white p-3 rounded-lg transition-colors shadow-md"
                    >
                        <Plus className="w-6 h-6" />
                    </button>
                </form>
                {error && <p className="text-red-500 text-center mt-2 text-sm font-bold animate-pulse">{error}</p>}

            </div>
        </div>
    );
}
