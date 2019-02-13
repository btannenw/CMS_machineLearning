
FROM jupyter/scipy-notebook

LABEL Name=cms_machinelearning Version=0.0.1

# Install 
RUN conda install --quiet --yes \
    'uproot' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
