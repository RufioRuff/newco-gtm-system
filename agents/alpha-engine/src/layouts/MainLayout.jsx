import React from 'react'

const MainLayout = ({ children }) => {
  return (
    <div style={{ minHeight: '100vh', background: '#0a0f1a' }}>
      {children}
    </div>
  )
}

export default MainLayout
