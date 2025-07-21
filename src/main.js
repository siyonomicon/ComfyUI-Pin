const app = new Function('return import("../../scripts/app.js")')();
const ComfyWidgets = new Function('return import("../../scripts/widgets.js")')();
import React from 'react';
import ReactDOM from 'react-dom/client';

// Create a React component
const PinGrid = ({ node }) => {
    const [imageUrls, setImageUrls] = React.useState([]);
    const [selectedImage, setSelectedImage] = React.useState(null);
    const ref = React.useRef(null);
    console.log(node)

    React.useEffect(() => {
        (async () => {
            await fetch("/pinterest_data")
                .then(response => response.json())
                .then(data => setImageUrls(data));
        })();
    }, []);

    const handleImageClick = async (url) => {
        setSelectedImage(url);
        node.widgets[0].value = url.replace(/\/236x\//, "/736x/");
        await fetch("/pin_grid_select_image", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ imageUrl: url.replace(/\/236x\//, "/736x/") }),
        });
    };

    return React.createElement(
        "div",
        {
            ref: ref,
            style: {
                display: "flex",
                flexWrap: "wrap",
            },
        },
        imageUrls.map(url =>
            React.createElement("img", {
                key: url,
                src: url.replace(/\/236x\//, "/736x/"),
                style: {
                    width: "33.33%",
                    flexBasis: "33.33%",
                    display: "block",
                    objectFit: "cover",
                    border: selectedImage === url ? "3px solid blue" : "none",
                    cursor: "pointer",
                },
                onClick: () => handleImageClick(url),
            })
        )
    );
};

Promise.all([
    app,
    ComfyWidgets
]).then(([{ app }, { ComfyWidgets }]) => {
    app.registerExtension({
        name: "Comfy.PinGridNode",
        async beforeRegisterNodeDef(nodeType, nodeData, app) {
            if (nodeData.name === "PinGridNode") {
                const onNodeCreated = nodeType.prototype.onNodeCreated;
                nodeType.prototype.onNodeCreated = function () {
                    onNodeCreated?.apply(this, arguments);

                    const grid = document.createElement("div");
                    grid.style.height = 'auto'
                    this.addDOMWidget("grid", "custom", grid, {
                        setValue: (value) => {
                            this.widgets[0].value = value;
                        }
                    });

                    const root = ReactDOM.createRoot(grid);
                    const el = React.createElement(PinGrid, {
                        node: this,
                    })

                    root.render(el);
                };
            }
        },
    })
});