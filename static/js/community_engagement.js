function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    const bgColor = type === 'error' ? 'bg-rose-600' : (type === 'success' ? 'bg-emerald-600' : 'bg-slate-800');

    toast.className = `${bgColor} text-white px-6 py-3 rounded-xl shadow-lg font-bold text-sm toast-animate-in flex items-center space-x-3`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="hover:opacity-75 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </button>
    `;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        toast.style.transition = 'all 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function handleVote(contentTypeId, objectId, value) {
    const csrfTokenEl = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenEl) {
        showToast("Please login to vote.", "error");
        return;
    }
    const csrftoken = csrfTokenEl.value;

    fetch('/questions/vote/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: `content_type_id=${contentTypeId}&object_id=${objectId}&value=${value}`
    })
        .then(response => {
            const isJson = response.headers.get('content-type')?.includes('application/json');
            if (!response.ok) {
                if (isJson) return response.json().then(err => { throw err; });
                if (response.status === 403 || response.status === 401) throw { error: "Please login to vote." };
                throw { error: "An error occurred. Please try again." };
            }
            return response.json();
        })
        .then(data => {
            const controls = document.querySelector(`.voting-controls[data-object-id="${objectId}"][data-content-type-id="${contentTypeId}"]`);
            if (controls) {
                controls.querySelector('.score').textContent = data.score;
                const upBtn = controls.querySelector('.upvote');
                const downBtn = controls.querySelector('.downvote');

                if (value === 1) {
                    if (data.action === 'added' || data.action === 'changed') {
                        upBtn.classList.add('text-indigo-600', 'bg-indigo-50');
                        downBtn.classList.remove('text-rose-600', 'bg-rose-50');
                    } else {
                        upBtn.classList.remove('text-indigo-600', 'bg-indigo-50');
                    }
                } else if (value === -1) {
                    if (data.action === 'added' || data.action === 'changed') {
                        downBtn.classList.add('text-rose-600', 'bg-rose-50');
                        upBtn.classList.remove('text-indigo-600', 'bg-indigo-50');
                    } else {
                        downBtn.classList.remove('text-rose-600', 'bg-rose-50');
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast(error.error || 'An error occurred while voting.', "error");
        });
}

function toggleComments(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.classList.toggle('hidden');
    }
}

function toggleReplyForm(commentId) {
    const form = document.getElementById(`reply-form-${commentId}`);
    if (form) {
        form.classList.toggle('hidden');
    }
}

function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        showToast("Link copied to clipboard!", "success");
    }).catch(() => {
        showToast("Failed to copy link.", "error");
    });
}
