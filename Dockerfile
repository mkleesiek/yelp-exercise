FROM jupyter/minimal-notebook

USER root

# libav-tools for matplotlib anim
RUN apt-get update && \
    apt-get install -y --no-install-recommends libav-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_USER

# Install Python 3 packages
# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
# use notebook-friendly backends in these images
RUN conda install --quiet --yes \
    'ipywidgets=5.2*' \
    'pandas=0.19*' \
    'matplotlib=1.5*' \
    'scipy=0.17*' \
    'seaborn=0.7*' \
    'scikit-learn=0.18*' \
    'simplejson=3.*' \
    && \
    conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy

# Activate ipywidgets extension in the environment that runs the notebook server
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /home/$NB_USER/.cache/
RUN MPLBACKEND=Agg python3 -c "import matplotlib.pyplot"

# Add project files
COPY JsonToCsvConverter.py ProcessTarFile.py YelpAnalysis.ipynb startup.sh $HOME/work/

# Make the entry script executable
USER root
RUN chmod +x $HOME/work/startup.sh
USER $NB_USER

# Expose Jupyter webinterface port
EXPOSE 8888

# Set working directory
WORKDIR $HOME/work

# Start default script through tini
ENTRYPOINT ["tini", "--"]
CMD ["./startup.sh"]
