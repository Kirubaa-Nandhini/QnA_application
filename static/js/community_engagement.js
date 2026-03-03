function handleVote(contentTypeId, objectId, value) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
                throw { error: "Migrations may not have been run. Please check the terminal." };
            }
            return response.json();
        })
        .then(data => {
            // Update the score display
            const controls = document.querySelector(`.voting-controls[data-object-id="${objectId}"][data-content-type-id="${contentTypeId}"]`);
            if (controls) {
                controls.querySelector('.score').textContent = data.score;

                // Toggle active classes
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
            if (error.error) {
                alert(error.error);
            } else {
                alert('An error occurred while voting. Please try again.');
            }
        });
}

function toggleComments(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.classList.toggle('hidden');
    }
}

function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = '<span class="text-emerald-500">Copied!</span>';
        setTimeout(() => {
            btn.innerHTML = originalText;
        }, 2000);
    });
}
