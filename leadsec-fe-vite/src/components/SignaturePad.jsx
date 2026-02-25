import React, { useRef } from 'react'
import SignatureCanvas from 'react-signature-canvas'
import './SignaturePad.css'

function SignaturePad({ onSignatureCapture }) {
  const sigCanvas = useRef()

  const handleClear = () => {
    sigCanvas.current.clear()
  }

  const handleSave = () => {
    if (sigCanvas.current.isEmpty()) {
      alert('Please provide a signature')
      return
    }
    const signatureData = sigCanvas.current.toDataURL()
    onSignatureCapture(signatureData)
  }

  return (
    <div className="signature-container">
      <h3>Client Signature</h3>
      <p className="signature-instruction">Please sign below</p>
      <div className="signature-pad-wrapper">
        <SignatureCanvas
          ref={sigCanvas}
          canvasProps={{
            className: 'signature-canvas',
            width: 400,
            height: 150
          }}
        />
      </div>
      <div className="signature-buttons">
        <button type="button" className="btn-secondary" onClick={handleClear}>
          Clear
        </button>
        <button type="button" className="btn-primary" onClick={handleSave}>
          Save Signature
        </button>
      </div>
    </div>
  )
}

export default SignaturePad
