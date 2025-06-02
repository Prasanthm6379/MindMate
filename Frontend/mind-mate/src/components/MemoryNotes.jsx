// src/components/MemoryNotes.jsx
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { memoryNoteAPI } from '../services/api';

export default function MemoryNotes() {
    const { user } = useAuth();
    const [notes, setNotes] = useState([]);
    const [newNote, setNewNote] = useState({
        title: '',
        content: '',
        file: null,
        type: 'note'
    });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadNotes();
    }, []);

    const loadNotes = async () => {
        setLoading(true);
        try {
            let user_id = sessionStorage.getItem('user_id')
            const data = await memoryNoteAPI.getAll(user_id);
            console.log(data);
            if (data.length == 0) {
                setNotes([]);
                return;
            }
            setNotes(data);
        } catch (error) {
            console.error('Error loading notes:', error);
        } finally {
            setLoading(false);
        }
    };

    const createNote = async (e) => {
        e.preventDefault();
        if (!newNote.title) return;

        try {
            if (newNote.type === 'img') {
                console.log(sessionStorage.getItem('user_id'));
                
                await memoryNoteAPI.create(sessionStorage.getItem('user_id'), {
                    title: newNote.title,
                    file: newNote.file
                }, true);
            } else {
                await memoryNoteAPI.create(sessionStorage.getItem('user_id'), {
                    title: newNote.title,
                    content: newNote.content
                });
            }
            setNewNote({ title: '', content: '', file: null, type: 'note' });
            await loadNotes();
        } catch (error) {
            console.error('Error creating note:', error);
        }
    };

    return (
        <div className="p-4 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-blue-600">Memory Notes</h1>

            <form onSubmit={createNote} className="mb-8 bg-white p-4 rounded-lg shadow-md">
                <input
                    type="text"
                    placeholder="Note title"
                    className="w-full p-2 mb-4 border-2 border-blue-200 rounded-lg text-xl"
                    value={newNote.title}
                    onChange={(e) => setNewNote({ ...newNote, title: e.target.value })}
                    required
                />

                <div className="mb-4">
                    <button
                        type="button"
                        className={`mr-2 p-2 ${newNote.type === 'note' ? 'bg-blue-600' : 'bg-gray-400'} text-white rounded-lg`}
                        onClick={() => setNewNote({ ...newNote, type: 'note' })}
                    >
                        Text Note
                    </button>
                    <button
                        type="button"
                        className={`p-2 ${newNote.type === 'img' ? 'bg-blue-600' : 'bg-gray-400'} text-white rounded-lg`}
                        onClick={() => setNewNote({ ...newNote, type: 'img' })}
                    >
                        Image Note
                    </button>
                </div>

                {newNote.type === 'img' ? (
                    <input
                        type="file"
                        onChange={(e) => setNewNote({ ...newNote, file: e.target.files[0] })}
                        className="mb-4"
                        required
                    />
                ) : (
                    <textarea
                        placeholder="Write your note..."
                        className="w-full p-2 mb-4 border-2 border-blue-200 rounded-lg text-xl h-32"
                        value={newNote.content}
                        onChange={(e) => setNewNote({ ...newNote, content: e.target.value })}
                        required
                    />
                )}

                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg text-xl hover:bg-blue-700 disabled:bg-gray-400"
                    disabled={loading}
                >
                    {loading ? 'Saving...' : 'Save Note'}
                </button>
            </form>

            {loading ? (
                <div className="text-center text-gray-600">Loading notes...</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {notes.map(note => (
                        <div key={note.id} className="bg-yellow-100 p-4 rounded-lg shadow-md">
                            <h3 className="text-xl font-bold mb-2">{note.title}</h3>
                            {note.note_type === 'img' ? (
                                <img src={note.content} alt="Memory" className="w-full h-48 object-cover rounded-lg" />
                            ) : (
                                <p className="text-lg">{note.content}</p>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}