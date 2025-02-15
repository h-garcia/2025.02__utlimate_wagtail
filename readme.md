# 2025.01.30 / Learn Wagtil / The Ultimate Wagtail Developers Course
https://github.com/KalobTaulien/ultimate-wagtail-developers-course-source-code 

## Run
* `pipenv shell`
* `python manage.py runserver`

## Lessons learned
* Custom image model
    * add a caption field or any needed field
    * https://docs.wagtail.org/en/stable/advanced_topics/images/image_file_formats.html
* Dynamic image serve view
    * This allows you to generate image URLs separately, speeding up the template rendering process.
    * https://learnwagtail.com/courses/the-ultimate-wagtail-developers-course/serving-dynamic-images/ 
    * https://docs.wagtail.org/en/stable/advanced_topics/images/image_serve_view.html#dynamic-image-serve-view 
* I can do a custom document model as well
    * https://docs.wagtail.org/en/stable/advanced_topics/documents/custom_document_model.html 
* BASE APP
    * CustomPageForm and validations
    * Configure a Tag snippet

## next
* Tests for admin pages and features