import './Source.css'
import React from 'react'
import { useEffect } from 'react'
import { HighlightWithinTextarea } from 'react-highlight-within-textarea'
import { scrollToHighlight } from './scroll'

const Source = ({ source, spanSelected }) => {
    // Functions are called once the components are rendered
    useEffect(() => {
        scrollToHighlight();
    }, []);

    // Building HTML
    return (
        <div className="source-container">
            <form id="sourceText" className="source-form" onSubmit={e => this.onSubmit(e)}>
                <HighlightWithinTextarea value={source} highlight={spanSelected} />
            </form>
        </div>
    )
}

export default Source
