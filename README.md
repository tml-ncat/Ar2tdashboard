# Rural Autonomous Vehicle Readiness Assessment Tool (Ar2tdashboard)

> **This tool has moved.** It now runs as a static page on the lab's GitHub Pages site:
> https://venktesh22.github.io/dashboards/Rural_AV_Readiness_Dashboard/Rural_AV_Readiness_Dashboard.html
>
> The Render service at `ar2tdashboard.onrender.com` now permanently redirects there, so existing
> links keep working. The original Dash application is preserved on the
> [`dash-app`](https://github.com/tml-ncat/Ar2tdashboard/tree/dash-app) branch.

This interactive dashboard assesses rural North Carolina communities' readiness for autonomous vehicle deployment across three key dimensions:

- **Physical Infrastructure**: Evaluates road conditions, bridges, and markings
- **Digital Infrastructure**: Measures network performance metrics
- **Social Vulnerability**: Considers transportation access and demographics

## Live Demo

Use the tool at [its new home on GitHub Pages](https://venktesh22.github.io/dashboards/Rural_AV_Readiness_Dashboard/Rural_AV_Readiness_Dashboard.html). The old address, [ar2tdashboard.onrender.com](https://ar2tdashboard.onrender.com), redirects there.

## Features

- Interactive county-level and census tract visualizations
- Customizable dimension weights
- Detailed metric comparisons between counties
- Comprehensive readiness scoring system
- Exportable insights and analytics

## Documentation

For detailed documentation and methodology, please visit the "Documentation" tab within the application.

## Running the original Dash app

The original Python/Dash version is preserved on the
[`dash-app`](https://github.com/tml-ncat/Ar2tdashboard/tree/dash-app) branch. To run it locally:

    git clone -b dash-app https://github.com/tml-ncat/Ar2tdashboard.git
    cd Ar2tdashboard
    pip install -r requirements.txt
    python src/app.py

Then open http://127.0.0.1:8050 in your browser.

## Citation
If you use this work in your research, please cite the following paper:

`Alaka, O. B., Pandey, V., & Khattak, A. (in press). Investigating Automated Shuttle Readiness for Rural Areas: A North Carolina Case Study. Transportation Research Record: Journal of the Transportation Research Board.`

## Acknowledgments

This research was supported by the Center for Rural and Regional Connected Communities (CR2C2), a Regional University Transportation Center funded by the United States Department of Transportation (USDOT). See Project 1-1 Information [Designing Tools for Assessing Readiness of Rural Communities for New Technologies](https://www.cr2c2.com/research/major-research-initiatives/mri-1/project-1-1).

## Contact

For questions or feedback, please contact Oladimeji Basit Alaka at obalaka@aggies.ncat.edu or Venktesh Pandey at vpandey@ncat.edu.

## Disclaimer

The views and accuracy of the information presented belong to the authors alone. The United States Department of Transportation assumes no liability for the contents or use thereof.
