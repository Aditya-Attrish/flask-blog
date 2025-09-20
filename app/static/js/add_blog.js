// Initialize Quill Editor
const quill = new Quill('#editor', {
    theme: 'snow',
    modules: {
        toolbar: [
            [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            [{ 'script': 'sub'}, { 'script': 'super' }],
            [{ 'indent': '-1'}, { 'indent': '+1' }],
            ['blockquote', 'code-block'],
            ['link', 'image', 'video'],
            [{ 'color': [] }, { 'background': [] }],
            [{ 'font': [] }],
            [{ 'align': [] }],
            ['clean']
        ]
    },
    placeholder: 'Write your amazing content here...'
});

// Update hidden input with editor content
quill.on('text-change', function() {
    document.getElementById('postContent').value = quill.root.innerHTML;
    updateStatistics();
});

// Featured Image Preview
document.getElementById('featuredImage').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('imagePreview');
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;

            // Update live preview
            document.getElementById('previewImage').innerHTML = `<img src="${e.target.result}" style="width: 100%; height: 100%; object-fit: cover;">`;
        };
        reader.readAsDataURL(file);
    }
});

// Character Counters
function setupCharacterCounter(inputId, counterId, maxLength) {
    const input = document.getElementById(inputId);
    const counter = document.getElementById(counterId);

    input.addEventListener('input', function() {
        const length = this.value.length;
        counter.textContent = `${length}/${maxLength} characters`;

        // Update warning colors
        if (length > maxLength * 0.8) {
            counter.className = 'character-count warning';
        } else if (length > maxLength) {
            counter.className = 'character-count danger';
        } else {
            counter.className = 'character-count';
        }

        // Update live preview
        updateLivePreview();
    });
}

setupCharacterCounter('postTitle', 'titleCount', 120);
setupCharacterCounter('postExcerpt', 'excerptCount', 300);
setupCharacterCounter('postMeta', 'metaCount', 160);

// Tag Input System
const tagInput = document.getElementById('tagInput');
const tagContainer = document.getElementById('tagContainer');
const postTags = document.getElementById('postTags');
const tags = [];

tagInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && this.value.trim()) {
        e.preventDefault();
        const tag = this.value.trim();
        if (!tags.includes(tag)) {
            tags.push(tag);
            updateTagsDisplay();
        }
        this.value = '';
    }
});

function updateTagsDisplay() {
    const tagsHtml = tags.map(tag => `
        <span class="tag">
            ${tag}
            <span class="tag-remove" onclick="removeTag('${tag}')">×</span>
        </span>
    `).join('');
    tagContainer.innerHTML = tagsHtml + '<input type="text" id="tagInput" class="border-0 w-auto" placeholder="Type and press Enter...">';
    postTags.value = tags.join(',');

    // Reattach event listener to new input
    document.getElementById('tagInput').addEventListener('keydown', tagInput.onkeydown);
}

function removeTag(tag) {
    const index = tags.indexOf(tag);
    if (index > -1) {
        tags.splice(index, 1);
        updateTagsDisplay();
    }
}

// Schedule Date Toggle
document.querySelectorAll('input[name="status"]').forEach(radio => {
    radio.addEventListener('change', function() {
        document.getElementById('scheduleField').style.display = 
            this.value === 'schedule' ? 'block' : 'none';
    });
});

// Auto-generate slug from title
document.getElementById('postTitle').addEventListener('input', function() {
    const slugInput = document.getElementById('postSlug');
    if (!slugInput.value) {
        const slug = this.value
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)/g, '');
        slugInput.value = slug;
        updateLivePreview();
    }
});

// Update statistics and live preview
function updateStatistics() {
    const text = quill.getText();
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const characters = text.length;
    const readTime = Math.ceil(words / 200); // Average reading speed

    document.getElementById('wordCount').textContent = words;
    document.getElementById('charCount').textContent = characters;
    document.getElementById('readTime').textContent = readTime;
    document.getElementById('previewReadTime').textContent = readTime + ' min read';
}

function updateLivePreview() {
    document.getElementById('previewTitle').textContent = document.getElementById('postTitle').value || 'Your post title will appear here';
    document.getElementById('previewExcerpt').textContent = document.getElementById('postExcerpt').value || 'Post excerpt will be shown here...';
    document.getElementById('previewCategory').textContent = document.getElementById('postCategory').value || 'Category';
    document.getElementById('previewUrl').textContent = 'blogsphere.com/blog/' + (document.getElementById('postSlug').value || 'your-post-url');
    document.getElementById('previewSeoTitle').textContent = document.getElementById('postTitle').value || 'Title';
    document.getElementById('previewMeta').textContent = document.getElementById('postMeta').value || 'Meta description will appear here...';
}

// Initialize live preview
updateLivePreview();

// Form validation
document.getElementById('blogForm').addEventListener('submit', function(e) {
    let valid = true;

    // Basic validation
    const requiredFields = ['title', 'excerpt', 'category', 'featured_image'];
    requiredFields.forEach(field => {
        const element = document.querySelector(`[name="${field}"]`);
        if (!element.value) {
            valid = false;
            element.classList.add('is-invalid');
        } else {
            element.classList.remove('is-invalid');
        }
    });

    // Content validation
    if (quill.getText().trim().length < 100) {
        valid = false;
        alert('Content must be at least 100 characters long');
    }

    if (!valid) {
        e.preventDefault();
        alert('Please fill in all required fields');
    }
});

// Preview button
document.getElementById('previewBtn').addEventListener('click', function() {
    alert('Preview functionality would open a new tab with your post preview');
    // In a real implementation, this would open a preview window
});