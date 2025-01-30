let selectedSongs = [];
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const selectedSongsList = document.getElementById('selectedSongs');
const songCount = document.getElementById('songCount');
const analysisDiv = document.getElementById('analysis');
const analysisText = document.getElementById('analysisText');
const analyzeButton = document.getElementById('analyzeButton');

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search for songs
const searchSongs = debounce(async (query) => {
    if (!query) {
        searchResults.classList.add('hidden');
        return;
    }

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const songs = await response.json();
        
        searchResults.innerHTML = songs.map(song => `
            <div class="p-3 hover:bg-gray-800 cursor-pointer flex items-center gap-3 border-b border-gray-700 last:border-0" 
                 onclick='selectSong(${JSON.stringify(song).replace(/'/g, "\\'")})'
            >
                <img 
                    src="${song.albumImage || '/static/default-album.png'}" 
                    alt="${song.album}" 
                    class="w-12 h-12 object-cover rounded-md"
                >
                <div>
                    <div class="font-medium text-gray-100">${song.name}</div>
                    <div class="text-sm text-gray-400">${song.artist}</div>
                </div>
            </div>
        `).join('');
        
        searchResults.classList.remove('hidden');
    } catch (error) {
        console.error('Search failed:', error);
    }
}, 300);

// Handle song selection
function selectSong(song) {
    if (selectedSongs.length >= 5) return;
    
    selectedSongs.push(song);
    updateSelectedSongsList();
    searchInput.value = '';
    searchResults.classList.add('hidden');
    
    // Enable/disable analyze button based on song count
    analyzeButton.disabled = selectedSongs.length !== 5;
}

// Update the selected songs list
function updateSelectedSongsList() {
    selectedSongsList.innerHTML = selectedSongs.map((song, index) => `
        <li class="flex justify-between items-center p-3 rounded-lg card-bg border border-gray-700">
            <div class="flex items-center gap-3">
                <img 
                    src="${song.albumImage || '/static/default-album.png'}" 
                    alt="${song.album}" 
                    class="w-12 h-12 object-cover rounded-md"
                >
                <div>
                    <div class="font-medium text-gray-100">${song.name}</div>
                    <div class="text-sm text-gray-400">${song.artist}</div>
                </div>
            </div>
            <button 
                onclick="removeSong(${index})" 
                class="text-gray-400 hover:text-red-400 transition-colors duration-200"
            >
                Remove
            </button>
        </li>
    `).join('');
    
    songCount.textContent = selectedSongs.length;
    
    // Update analyze button state
    analyzeButton.disabled = selectedSongs.length !== 5;
}

// Remove a song from the selection
function removeSong(index) {
    selectedSongs.splice(index, 1);
    updateSelectedSongsList();
    analysisDiv.classList.add('hidden');
}

// Analyze personality
async function analyzePersonality() {
    analyzeButton.disabled = true;
    analyzeButton.textContent = 'Analyzing...';
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(selectedSongs)
        });
        
        const data = await response.json();
        // Use marked to render Markdown
        const analysisHtml = marked.parse(data.analysis);
        analysisText.innerHTML = analysisHtml;  // Use innerHTML instead of textContent
        analysisDiv.classList.remove('hidden');
    } catch (error) {
        console.error('Analysis failed:', error);
        alert('Failed to analyze songs. Please try again.');
    } finally {
        analyzeButton.disabled = selectedSongs.length !== 5;
        analyzeButton.textContent = 'Analyze My Music Taste';
    }
}

// Event listeners
searchInput.addEventListener('input', (e) => searchSongs(e.target.value));
analyzeButton.addEventListener('click', analyzePersonality); 