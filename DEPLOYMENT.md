# Deployment Guide for Hugging Face Spaces

This guide will help you deploy the Automated Test Case Generator to Hugging Face Spaces.

## Prerequisites

- A Hugging Face account (create one at https://huggingface.co/join)
- Git installed on your local machine
- Python 3.10+ installed

## Step-by-Step Deployment

### Option 1: Deploy via Hugging Face Web Interface (Easiest)

1. **Create a New Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Fill in the details:
     - **Space name**: test-case-generator (or your preferred name)
     - **License**: MIT
     - **Select the SDK**: Gradio
     - **Space hardware**: CPU basic (free) or GPU for faster performance
     - **Visibility**: Public or Private

2. **Upload Files**
   - After creating the space, you'll see a file upload interface
   - Upload all files from your project:
     - `app.py`
     - `test_case_generator.py`
     - `requirements.txt`
     - `README.md` (this will be auto-detected as the Space description)

3. **Wait for Build**
   - Hugging Face will automatically detect your files and start building
   - This may take 5-10 minutes for the first build
   - You can see the build logs in the "Logs" tab

4. **Access Your Space**
   - Once built, your space will be available at:
     `https://huggingface.co/spaces/YOUR_USERNAME/test-case-generator`

### Option 2: Deploy via Git (Advanced)

1. **Create a New Space on Hugging Face**
   - Follow step 1 from Option 1

2. **Clone the Space Repository**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/test-case-generator
   cd test-case-generator
   ```

3. **Copy Your Files**
   ```bash
   # Copy all project files to the cloned repository
   cp /path/to/your/project/* .
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Initial deployment of test case generator"
   git push
   ```

5. **Monitor Build**
   - Go to your space URL and check the logs
   - Wait for the build to complete

## Configuration Options

### Choosing Hardware

For optimal performance, consider these hardware options:

- **CPU Basic (Free)**: Good for testing, slower generation (30-60 seconds per request)
- **CPU Upgrade**: Faster CPU, better for production (15-30 seconds)
- **GPU T4 (Paid)**: Best performance, fastest generation (5-10 seconds)
- **GPU A10G (Paid)**: Best for 13B model, very fast (3-5 seconds)

To upgrade hardware:
1. Go to your Space settings
2. Click "Settings" → "Resource"
3. Select your preferred hardware tier

### Model Selection

You can change the default model in `app.py` line 168:

```python
# Change this line to use a different default model
model_choice = "CodeLlama 13B (Better)"  # or "Mistral 7B"
```

### Memory Optimization

If you encounter out-of-memory errors:

1. **Use 8-bit quantization** (already enabled in test_case_generator.py)
2. **Reduce max_tokens** in test_case_generator.py:
   ```python
   # Line 95 - reduce from 2048 to 1024
   def generate_test_cases(self, problem_description: str, max_tokens: int = 1024):
   ```
3. **Use smaller model**: Stick with CodeLlama 7B instead of 13B

## Testing Your Deployment

1. **Access your Space URL**
2. **Try the example problems** provided in the interface
3. **Test with custom problems**
4. **Verify JSON output** is properly formatted
5. **Test the download functionality**

## Troubleshooting

### Issue: Build Fails

**Solution**: Check the build logs for errors. Common issues:
- Missing dependencies → Update `requirements.txt`
- Incompatible package versions → Pin specific versions
- Out of memory → Reduce model size or upgrade hardware

### Issue: Model Takes Too Long to Load

**Solution**: 
- The first request will be slow as the model downloads
- Subsequent requests will be faster (model cached)
- Consider using GPU hardware for faster inference

### Issue: Out of Memory Error

**Solution**:
- Use CPU basic hardware with CodeLlama 7B only
- Or upgrade to GPU hardware
- Enable 8-bit quantization (already enabled)

### Issue: JSON Output is Malformed

**Solution**:
- Increase temperature in test_case_generator.py line 97
- Adjust the prompt to be more specific
- Use a larger model (13B instead of 7B)

## Updating Your Space

### Via Web Interface
1. Go to your Space → Files
2. Click on the file you want to update
3. Edit and commit changes

### Via Git
```bash
cd test-case-generator
# Make your changes
git add .
git commit -m "Update: describe your changes"
git push
```

## Cost Considerations

- **Free Tier**: CPU basic (with some limitations on uptime)
- **Paid Tiers**: 
  - CPU Upgrade: ~$0.03/hour
  - GPU T4: ~$0.60/hour
  - GPU A10G: ~$3.15/hour

**Recommendation**: Start with free tier for testing, upgrade to GPU if you need faster performance.

## Making Your Space Public

To share your space:
1. Go to Space Settings
2. Change visibility to "Public"
3. Share the URL: `https://huggingface.co/spaces/YOUR_USERNAME/test-case-generator`

## Advanced: Custom Domain

Hugging Face Spaces supports custom domains:
1. Go to Space Settings → Custom Domain
2. Follow the DNS configuration instructions
3. Your space will be available at your custom domain

## Support

- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Gradio Docs: https://gradio.app/docs/
- Issues: Create an issue in your Space repository

## Next Steps

After deployment:
1. Monitor usage and performance
2. Collect user feedback
3. Fine-tune prompts for better results
4. Consider fine-tuning the model on domain-specific data
5. Add more example problems
6. Integrate with your evaluation pipeline

## Security Notes

- Never commit API keys or secrets
- Use Hugging Face Secrets for sensitive data
- Keep your Space updated with security patches
- Monitor for unusual activity

---

Happy Deploying!
