// ===== START CUSTOM DATA =====
const DATA = {
    STYLE: {
        NB_MAX_CONTRIBUTORS_PER_LINE: 3, // Integer in [1, 2, 3, 4, 6]
        CONTRIBUTOR_IMAGE_SIZE: "180px",
        FOOTER_LOGO_SIZE: "240px",
    },
    HEAD: {
        FAVICON_SRC: "img/logo_dummy.png",
        PROJECT_TITLE: "Like, Comment, Get Scammed: Characterizing Comment Scams on Media Platforms",
        PROJECT_SUBTITLE: {
            "name": "Network and Distributed Systems Security (NDSS) Symposium 2024",
            "url": "https://www.ndss-symposium.org/ndss2024/",
        },
        AUTHOR_NAME: "Xigao Li",
        VIDEO_SRC: "video/dummy_video.mp4",
    },
    ABSTRACT: {
        TEXT: [
            "Given the meteoric rise of large media platforms (such as YouTube) on the web, it is no surprise that attackers seek to abuse them in order to easily reach hundreds of millions of users. Among other social-engineering attacks perpetrated on these platforms, comment scams have increased in popularity despite the presence of mechanisms that purportedly give content creators control over their channel comments. In a comment scam, attackers set up script-controlled accounts that automatically post or reply to comments on media platforms, enticing users to contact them. Through the promise of free prizes and investment opportunities, attackers aim to steal financial assets from the end users that contact them.",
            "In this paper, we present the first systematic, large-scale study of comment scams. We design and implement an infrastructure to collect a dataset of 8.8 million comments from 20 different YouTube channels over a 6-month period. We develop filters based on textual, graphical, and temporal features of comments and identify 206K scam comments from 10K unique accounts. Using this dataset, we present our analysis of scam campaigns, comment dynamics, and evasion techniques used by scammers.",
            "Lastly, through an IRB-approved study, we interact with 50 scammers to gain insights into their social-engineering tactics and payment preferences. Using transaction records on public blockchains, we perform a quantitative analysis of the financial assets stolen by scammers finding that just the scammers that were part of our user study have stolen funds equivalent to millions of dollars. Our study demonstrates that existing scam-detection mechanisms are insufficient for curbing abuse, pointing to the need for better comment-moderation tools as well as other changes that would make it difficult for attackers to obtain tens of thousands of accounts on these large platforms."
],
        // OVERVIEW: {
        //     "src": "img/overview_dummy.png",
        //     "legend": "Dummy overview of our method.",
        // }
    },
    CONTENT: [ // If you want to add other sections, add them with their title (used for navigation) and the html code of the section
        // {
        //     "name": "Section 1",
        //     "html": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra finibus quam, nec ornare mi posuere id. Nullam vitae efficitur neque. Maecenas rutrum nunc sit amet rhoncus iaculis. Pellentesque rutrum at nisl vitae dapibus. Maecenas auctor faucibus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vestibulum a leo porttitor, mollis diam id, porta odio. Donec convallis porttitor lectus sed fringilla. Nulla facilisi. Curabitur tincidunt turpis sit amet leo lobortis lacinia.",
        // },
        // {
        //     "name": "Section 2",
        //     "html": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra finibus quam, nec ornare mi posuere id. Nullam vitae efficitur neque. Maecenas rutrum nunc sit amet rhoncus iaculis. Pellentesque rutrum at nisl vitae dapibus. Maecenas auctor faucibus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vestibulum a leo porttitor, mollis diam id, porta odio. Donec convallis porttitor lectus sed fringilla. Nulla facilisi. Curabitur tincidunt turpis sit amet leo lobortis lacinia.",
        // },
    ],
    CONTRIBUTORS: [
        {
            "name": "Xigao Li",
            "img": "img/xigao_2031_sq.png",
            "url": "https://xigaoli.com"
        },
        {
            "name": "Amir Rahmati",
            "img": "img/amir.jpg",
            "url": "https://amir.rahmati.com"
        },
        {
            "name": "Nick Nikiforakis",
            "img": "img/nick_new_small.jpg",
            "url": "https://securitee.org"
        },
    ],
    LINKS: [
        {
            "title": "Paper",
            "icon": "img/paper.svg",
            "links": [
                {
                    "name": "PDF",
                    "url": "paper/youtube_scam_paper-23nov16.pdf",
                    "icon": "img/paper_copy.svg"
                },
            ],
        },
        {
            "title": "Code",
            "icon": "img/code.svg",
            "links": [
                {
                    "name": "Access Crawler Code",
                    "id": "accessButton",
                    "url": "#",
                    "icon": "img/GitHub-Mark-Light-32px.png"
                },
                // {
                //     "name": "Example Video:<br> Cryptocurrency Giveaway Scam",
                //     "url": "#",
                //     "icon": "img/GitHub-Mark-Light-32px.png"
                // },
            ],
        },
        
    ],
    CITATION: ` \
        @article{xigao2024comment,
            title     = {Like, Comment, Get Scammed: Characterizing Comment Scams on Media Platforms},
            author    = {Li, Xigao and Rahmati, Amir and Nikiforakis, Nick},
            booktitle = {Network and Distributed Systems Security (NDSS) Symposium},
            year      = {2024}
        }
    `,
    FOOTER: {
        LOGOS: [
            {
                "name": "PragSec Lab",
                "src": "img/pragsec.png",
                "url": "https://www.securitee.org/"
            },
            {
                "name": "Ethos Lab",
                "src": "img/ethos.png",
                "url": "https://github.com/Ethos-lab"
            },
            {
                "name": "Stony Brook University",
                "src": "img/sbu.png",
                "url": "#"
            },
        ],
        COPYRIGHT: `Copyright PragSec Lab & Ethos Lab 2023`
    },
}
// ===== END CUSTOM DATA =====




// /!\ --- Do not change following lines ---

const NB_COLS = 12;
const section_links_nav = DATA.CONTENT.map(section => ({ "id": idFromTitle(section), "name": section.name }));
const NAVIGATION_LINKS = [{ "id": "abstract", "name": "Abstract" }].concat(
    DATA.CONTENT.map(section => ({ "id": idFromTitle(section), "name": section.name })),
    [
        { "id": "contributors", "name": "Contributors" },
        { "id": "links", "name": "Links" }
    ]
);


/* Utils */
function link(url, content, style = ``) {
    return `<a href=${url} target="_blank" ${style}>${content}</a>`;
}

function padding(nbElements, nbElementsMax) {
    const PADDING_COLS = (NB_COLS - nbElements * Math.floor(NB_COLS / nbElementsMax)) / 2;
    return PADDING_COLS > 0 ? `<div class=col-lg-${PADDING_COLS}></div>` : ``;
}

function idFromTitle(title) {
    return title.name.toLowerCase().replace(' ', '-');
}

/* Header */
function displayTitle() {
    let oneLineTitle = DATA.HEAD.PROJECT_TITLE;
    const remove = ["<br>", "<br/>", "<br />"];
    for (const val of remove) {
        oneLineTitle = oneLineTitle.replace(val, " ");
    }
    document.head.querySelector("title").innerHTML = oneLineTitle;
    document.head.querySelector("meta[name='author']").content = DATA.HEAD.AUTHOR_NAME;
    document.head.querySelector("meta[name='description']").content = oneLineTitle;

    document.head.querySelector("link[rel='icon']").type = `image/${DATA.HEAD.FAVICON_SRC.split(".").at(-1)}`;
    document.head.querySelector("link[rel='icon']").href = DATA.HEAD.FAVICON_SRC;

    document.getElementById("nav-project-title").innerHTML = oneLineTitle;
    document.getElementById("head-title").innerHTML = DATA.HEAD.PROJECT_TITLE;
    document.getElementById("head-subtitle").innerHTML = `<a href=${DATA.HEAD.PROJECT_SUBTITLE.url}>${DATA.HEAD.PROJECT_SUBTITLE.name}</a>`;
}

function displayNav() {
    document.getElementById("navigation").innerHTML = NAVIGATION_LINKS.map(
        link => `
        <li class="nav-item">
            <a class="nav-link active" href="#${link.id}">${link.name}</a>
        </li>
    `).join("");
}

/* Video section */
function displayVideo() {
    document.getElementById("video").innerHTML = `<iframe class="embed-responsive-item" src=${DATA.HEAD.VIDEO_SRC}></iframe>`;
}

/* Abstract section */
function displayAbstract() {
    document.getElementById("abstract-text").innerHTML = `
    <div class="col-sm">
        <h2 class="text-center">Abstract</h2>
        <hr>
        ${DATA.ABSTRACT.TEXT.map(text => `<p>${text}</p>`).join("")}
        <br>
    </div>
  `;
}

function displayOverview() {
    document.getElementById("overview").innerHTML = `
        <div class="col-sm">
            <img src=${DATA.ABSTRACT.OVERVIEW.src} alt="Method Overview" class="img-fluid">
            <div id="overview-legend">${DATA.ABSTRACT.OVERVIEW.legend}</div>
        </div>
    `;
}

/* Content sections */
function displayContentSections() {
    document.getElementById("content").innerHTML = DATA.CONTENT.map(
        section => `
        <div class="container section" id=${idFromTitle(section)}>
            <div class="row">
                <div class="col-sm">
                    <h2 class="text-center">${section.name}</h2>
                    <hr>
                    ${section.html}
                </div>
            </div>
        </div>
        `
    ).join("");
}

/* Contributors section */
function addPadding(nbContributorsInLine) {
    return padding(nbContributorsInLine, DATA.STYLE.NB_MAX_CONTRIBUTORS_PER_LINE);
}

function displayContributorsRow(contributorsInRow) {
    let htmlContent = `<div class="row text-center">` + addPadding(contributorsInRow.length);

    for (const contributor of contributorsInRow) {
        const htmlImg = `<img class="rounded-circle" src=${contributor.img} alt=${contributor.name} width=${DATA.STYLE.CONTRIBUTOR_IMAGE_SIZE} height=${DATA.STYLE.CONTRIBUTOR_IMAGE_SIZE} />`;
        htmlContent +=
            `<div class="col-lg-${Math.floor(NB_COLS / DATA.STYLE.NB_MAX_CONTRIBUTORS_PER_LINE)}">
                ${link(contributor.url, htmlImg)}
                <h4>${link(contributor.url, contributor.name)}</h4>
            </div>`;
    }
    htmlContent += addPadding(contributorsInRow.length) + `</div>`;
    return htmlContent;
}

function displayContributors() {
    htmlContent = "";

    nbLines = Math.ceil(DATA.CONTRIBUTORS.length / DATA.STYLE.NB_MAX_CONTRIBUTORS_PER_LINE)
    for (const rowId of Array(nbLines).keys()) {
        const contributorsInRow = DATA.CONTRIBUTORS.slice(rowId * DATA.STYLE.NB_MAX_CONTRIBUTORS_PER_LINE, (rowId + 1) * DATA.STYLE.NB_MAX_CONTRIBUTORS_PER_LINE);
        htmlContent += displayContributorsRow(contributorsInRow);
    }

    document.getElementById("contributors").innerHTML += htmlContent;
}


/* Links section */
function formatLink(_link) {
    return `<div class="col-sm text-center">
            ${link(_link.url, `<img src=${_link.icon} width="20px"> ${_link.name}`, `role="button" class="btn btn-dark" id=${"id" in _link?_link.id:""}`)}
        </div>`;
}

function formatLinkGroup(group) {
    return `<div class="col-sm text-center">
                <img src=${group.icon} />
                <h4>${group.title}</h4>
                ${group.links.map(link => formatLink(link)).join("")}
            </div>`;
}

function displayLinks() {
    document.getElementById("links-area").innerHTML = DATA.LINKS.map(
        group => formatLinkGroup(group)
    ).join("");
}

/* Citation */
function displayCitation() {
    htmlContent = `<code>${DATA.CITATION}</code>`;
    document.getElementsByClassName("citation")[0].innerHTML = htmlContent;
}

/* Footer */
function displayFooter() {
    const nbLogos = DATA.FOOTER.LOGOS.length;
    const nbColsPerDiv = Math.floor(NB_COLS / (nbLogos + 1));
    const pad = padding(nbLogos + 1, nbLogos + 1);

    const htmlLogos = DATA.FOOTER.LOGOS.map(logo => `\
        <div class="col-md-${nbColsPerDiv} text-center">
            ${link(logo.url, `<img src=${logo.src} alt=${logo.name} width=${DATA.STYLE.FOOTER_LOGO_SIZE}>`)}
        </div>
    `);

    document.getElementById("footer").innerHTML = `\
        <div class="container footer-container">
            <div class="row align-items-center h-100">
                ${pad}
                ${htmlLogos.join("")}
                <div class="col-md-${nbColsPerDiv} text-center align-middle">
                    <h5>&copy; ${DATA.FOOTER.COPYRIGHT}</h5>
                    Website Design: ${link("https://github.com/rjgpinel/dark-academic-website", "dark-academic-website")}
                </div>
                ${pad}
            </div>
        </div>
    `;
}

function loadConsent() {
    document.getElementById('accessButton').addEventListener('click', function() {
    document.getElementById('consentModal').style.display = 'block';
    });

    document.getElementById('consentCheckbox').checked = false;
    document.getElementById('consentCheckbox').addEventListener('change', function() {
        document.getElementById('confirmButton').disabled = !this.checked;
    });

    document.getElementById('confirmButton').addEventListener('click', function() {
        window.location.href = 'https://github.com/like-comment-get-scammed/like-comment-get-scammed.github.io/tree/main/code';
        document.getElementById('consentModal').style.display = 'none';
    });
}

/* Main */
function displayPage() {
    displayTitle();
    displayNav();
    // displayVideo();
    displayAbstract();
    // displayOverview();
    // displayContentSections();
    displayContributors();
    displayLinks();
    loadConsent();
    displayCitation();
    displayFooter();
}

displayPage();
