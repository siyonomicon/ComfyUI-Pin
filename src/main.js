const app = new Function('return import("../../scripts/app.js")')();
import React from 'react';
import ReactDOM from 'react-dom/client';

// Create a React component
const PinGrid = () => {
    const [imageUrls, setImageUrls] = React.useState([]);

    React.useEffect(async () => {
        const response = await fetch("/pin_grid_images")
            .then(response => response.json())
            .then(data => setImageUrls(data));
    }, []);

    return React.createElement(
        "div",
        {
            style: {
                display: "flex",
                flexWrap: "wrap",
            },
        },
        imageUrls.map(url =>
            React.createElement("img", {
                key: url,
                src: url,
                style: {
                    width: "33.33%",
                    flexBasis: "33.33%",
                    height: "100%",
                    display: "block",
                    objectFit: "cover",
                },
            })
        )
    );
};


app.then(({ app }) => {
    app.registerExtension({
        name: "Comfy.PinGridNode",
        async beforeRegisterNodeDef(nodeType, nodeData, app) {
            if (nodeData.name === "PinGridNode") {
                const onNodeCreated = nodeType.prototype.onNodeCreated;
                nodeType.prototype.onNodeCreated = function () {
                    onNodeCreated?.apply(this, arguments);

                    const grid = document.createElement("div");
                    this.addDOMWidget("grid", "grid", grid);

                    const root = ReactDOM.createRoot(grid);
                    root.render(React.createElement(PinGrid));
                };
            }
        },
    })
});