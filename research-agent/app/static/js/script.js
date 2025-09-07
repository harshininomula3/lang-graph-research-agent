class ResearchApp {
    constructor() {
        this.currentResearchId = null;
        this.initializeEventListeners();
        this.loadResearchHistory();
    }

    initializeEventListeners() {
        // Research form submission
        document.getElementById('researchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.startResearch();
        });

        // Download report
        document.getElementById('downloadBtn').addEventListener('click', () => {
            this.downloadReport();
        });

        // New research
        document.getElementById('newResearchBtn').addEventListener('click', () => {
            this.showResearchForm();
        });
    }

    async startResearch() {
        const topic = document.getElementById('topic').value;
        const questionsText = document.getElementById('questions').value;
        const questions = questionsText.split('\n').filter(q => q.trim());

        if (!topic || questions.length === 0) {
            this.showError('Please provide a topic and at least one research question.');
            return;
        }

        try {
            // Show progress section
            this.showProgress(topic, questions);

            // Start research via API
            const response = await fetch('/api/research', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topic, questions })
            });

            if (!response.ok) {
                throw new Error('Failed to start research');
            }

            const data = await response.json();
            this.currentResearchId = data.research_id;

            // Start polling for results
            this.pollResearchStatus();

        } catch (error) {
            this.showError(error.message);
        }
    }

    async pollResearchStatus() {
        if (!this.currentResearchId) return;

        try {
            const response = await fetch(`/api/research/${this.currentResearchId}`);
            const status = await response.json();

            if (status.status === 'completed') {
                this.showResults(status);
                this.loadResearchHistory();
            } else if (status.status === 'error') {
                this.showError(status.error);
            } else {
                // Update progress and continue polling
                this.updateProgress(status);
                setTimeout(() => this.pollResearchStatus(), 2000);
            }
        } catch (error) {
            this.showError('Error checking research status');
        }
    }

    showProgress(topic, questions) {
        // Hide other sections
        this.hideAllSections();

        // Show progress section
        document.getElementById('progressSection').classList.remove('hidden');

        // Update progress content
        document.getElementById('currentTopic').textContent = topic;
        
        const questionsList = document.getElementById('questionsList');
        questionsList.innerHTML = questions.map(q => 
            `<li>${q}</li>`
        ).join('');

        // Reset progress bar
        document.querySelector('.progress-fill').style.width = '0%';
        document.getElementById('progressText').textContent = 'Initializing research agent...';
    }

    updateProgress(status) {
        // Simulate progress (in real app, you might have actual progress indicators)
        const progressBar = document.querySelector('.progress-fill');
        const progressText = document.getElementById('progressText');
        
        // Animate progress bar
        const currentWidth = parseInt(progressBar.style.width) || 0;
        const newWidth = Math.min(currentWidth + 10, 90);
        progressBar.style.width = newWidth + '%';
        
        progressText.textContent = 'Research in progress...';
    }

    showResults(results) {
        this.hideAllSections();
        
        // Show results section
        document.getElementById('resultsSection').classList.remove('hidden');
        
        // Display report
        document.getElementById('reportContent').textContent = results.report;
        
        // Complete progress bar
        document.querySelector('.progress-fill').style.width = '100%';
    }

    async downloadReport() {
        if (!this.currentResearchId) return;

        try {
            const response = await fetch(`/api/research/${this.currentResearchId}/report`);
            const data = await response.json();

            // Create download link
            const blob = new Blob([data.report], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `research_report_${data.topic.replace(/\s+/g, '_')}.txt`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

        } catch (error) {
            this.showError('Error downloading report');
        }
    }

    showResearchForm() {
        this.hideAllSections();
        document.getElementById('researchForm').reset();
    }

    showError(message) {
        this.hideAllSections();
        document.getElementById('errorSection').classList.remove('hidden');
        document.getElementById('errorMessage').textContent = message;
    }

    hideError() {
        document.getElementById('errorSection').classList.add('hidden');
    }

    hideAllSections() {
        document.getElementById('progressSection').classList.add('hidden');
        document.getElementById('resultsSection').classList.add('hidden');
        document.getElementById('errorSection').classList.add('hidden');
    }

    async loadResearchHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            this.displayHistory(data.history);
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    displayHistory(history) {
        const historyList = document.getElementById('historyList');
        
        if (history.length === 0) {
            historyList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-history"></i>
                    <p>No research history yet</p>
                </div>
            `;
            return;
        }

        historyList.innerHTML = history.map(item => `
            <div class="history-item ${item.status}">
                <h4>${item.topic}</h4>
                <p>Status: ${item.status}</p>
                <small>Started: ${new Date(item.started_at).toLocaleString()}</small>
            </div>
        `).join('');
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ResearchApp();
});

// Helper function to hide error
function hideError() {
    document.getElementById('errorSection').classList.add('hidden');
}
