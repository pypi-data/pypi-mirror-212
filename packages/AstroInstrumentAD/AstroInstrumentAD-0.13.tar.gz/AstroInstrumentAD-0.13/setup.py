from distutils.core import setup
setup(
  name = 'AstroInstrumentAD',         # How you named your package folder (MyLib)
  packages = ['AstroInstrumentAD'],   # Chose the same as "name"
  version = '0.13',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  author = 'Jay Stephan',                   # Type in your name
  author_email = 'Jay.Stephan@stfc.ac.uk',      # Type in your E-Mail
  url = 'https://github.com/JamianStephan/AstroInstrumentAD',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/JamianStephan/AstroInstrumentAD/archive/refs/tags/v0.1.zip',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'matplotlib',
          'astropy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',      #Specify which pyhton versions that you want to support

  ],
)