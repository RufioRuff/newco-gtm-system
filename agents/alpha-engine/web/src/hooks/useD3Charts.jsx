// ════════════════════════════════════════════════════
// D3 VISUALIZATION HOOKS — Reusable chart components
// Each returns a ref to attach to an SVG container
// ════════════════════════════════════════════════════
import { useEffect, useRef, useCallback } from 'react'
import * as d3 from 'd3'
import { theme as T, fonts, chartColors, tierColors } from 'src/lib/theme'

const { mono } = fonts

// ═══ FORCE-DIRECTED NETWORK GRAPH ═══
export function useForceGraph(containerRef, { nodes, edges, width, height, onNodeClick }) {
  useEffect(() => {
    if (!containerRef.current || !nodes?.length) return

    const svg = d3.select(containerRef.current)
    svg.selectAll('*').remove()

    const g = svg.append('g')

    // Zoom
    svg.call(d3.zoom().scaleExtent([0.3, 4]).on('zoom', (e) => g.attr('transform', e.transform)))

    // Force simulation
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(edges).id(d => d.id).distance(80))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(d => (d.size || 8) + 4))

    // Concentric rings
    const rings = [0.25, 0.5, 0.75, 1]
    rings.forEach(r => {
      g.append('circle')
        .attr('cx', width / 2).attr('cy', height / 2)
        .attr('r', Math.min(width, height) * 0.4 * r)
        .attr('fill', 'none').attr('stroke', T.border).attr('stroke-width', 0.5)
        .attr('stroke-dasharray', '2,4').attr('opacity', 0.4)
    })

    // Links
    const link = g.selectAll('.link').data(edges).enter()
      .append('line').attr('class', 'link')
      .attr('stroke', T.border).attr('stroke-width', 0.5).attr('opacity', 0.3)

    // Nodes
    const node = g.selectAll('.node').data(nodes).enter()
      .append('g').attr('class', 'node').style('cursor', 'pointer')
      .call(d3.drag()
        .on('start', (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y })
        .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y })
        .on('end', (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null })
      )

    node.append('circle')
      .attr('r', d => d.size || 6)
      .attr('fill', d => tierColors[d.tier] || T.accent)
      .attr('opacity', 0.8)
      .attr('stroke', d => tierColors[d.tier] || T.accent)
      .attr('stroke-width', 1)

    // Labels for large nodes
    node.filter(d => (d.size || 6) > 8)
      .append('text')
      .text(d => d.label?.slice(0, 12) || '')
      .attr('dy', d => (d.size || 6) + 12)
      .attr('text-anchor', 'middle')
      .attr('fill', T.textMuted).attr('font-size', 8).attr('font-family', mono)

    // Hover effects
    node.on('mouseenter', function(e, d) {
      d3.select(this).select('circle').transition().duration(150)
        .attr('r', (d.size || 6) + 3).attr('opacity', 1)
      link.attr('opacity', l => (l.source.id === d.id || l.target.id === d.id) ? 0.6 : 0.05)
    }).on('mouseleave', function(e, d) {
      d3.select(this).select('circle').transition().duration(150)
        .attr('r', d.size || 6).attr('opacity', 0.8)
      link.attr('opacity', 0.3)
    }).on('click', (e, d) => onNodeClick?.(d))

    // Tick
    simulation.on('tick', () => {
      link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d => d.target.y)
      node.attr('transform', d => `translate(${d.x},${d.y})`)
    })

    return () => simulation.stop()
  }, [nodes, edges, width, height])
}

// ═══ SPIDER / RADAR CHART ═══
export function useRadarChart(containerRef, { data, axes, size = 140, color }) {
  useEffect(() => {
    if (!containerRef.current || !data || !axes) return

    const svg = d3.select(containerRef.current)
    svg.selectAll('*').remove()

    const cx = size / 2, cy = size / 2, r = size / 2 - 16
    const angleSlice = (Math.PI * 2) / axes.length
    const g = svg.append('g').attr('transform', `translate(${cx},${cy})`)
    const rScale = d3.scaleLinear().domain([0, 100]).range([0, r])
    const fillColor = color || T.accent

    // Grid rings
    ;[25, 50, 75, 100].forEach(level => {
      g.append('circle').attr('r', rScale(level))
        .attr('fill', 'none').attr('stroke', T.border).attr('stroke-width', 0.5)
    })

    // Axis lines
    axes.forEach((_, i) => {
      const angle = angleSlice * i - Math.PI / 2
      g.append('line')
        .attr('x1', 0).attr('y1', 0)
        .attr('x2', Math.cos(angle) * r).attr('y2', Math.sin(angle) * r)
        .attr('stroke', T.border).attr('stroke-width', 0.5)
    })

    // Data polygon
    const radarLine = d3.lineRadial()
      .radius(d => rScale(d))
      .angle((_, i) => i * angleSlice)
      .curve(d3.curveCardinalClosed.tension(0.3))

    const path = g.append('path')
      .datum([...data, data[0]])
      .attr('d', radarLine)
      .attr('fill', `${fillColor}20`).attr('stroke', fillColor)
      .attr('stroke-width', 1.5).attr('opacity', 0)

    path.transition().duration(800).ease(d3.easeBackOut).attr('opacity', 1)

    // Score dots
    data.forEach((val, i) => {
      const angle = angleSlice * i - Math.PI / 2
      g.append('circle')
        .attr('cx', Math.cos(angle) * rScale(val))
        .attr('cy', Math.sin(angle) * rScale(val))
        .attr('r', 0).attr('fill', fillColor)
        .transition().delay(400 + i * 100).duration(400).ease(d3.easeBackOut)
        .attr('r', 3)
    })

    // Axis labels
    axes.forEach((label, i) => {
      const angle = angleSlice * i - Math.PI / 2
      const lx = Math.cos(angle) * (r + 12)
      const ly = Math.sin(angle) * (r + 12)
      g.append('text')
        .attr('x', lx).attr('y', ly)
        .attr('text-anchor', 'middle').attr('dominant-baseline', 'middle')
        .attr('fill', T.textDim).attr('font-size', 7).attr('font-family', mono)
        .text(label.slice(0, 3).toUpperCase())
    })

    // Center score
    const avg = Math.round(data.reduce((a, b) => a + b, 0) / data.length)
    const scoreText = g.append('text')
      .attr('text-anchor', 'middle').attr('dominant-baseline', 'middle')
      .attr('fill', fillColor).attr('font-size', 16).attr('font-weight', 800).attr('font-family', mono)

    scoreText.transition().duration(1000).ease(d3.easeCubicOut)
      .tween('text', function() {
        const interp = d3.interpolateNumber(0, avg)
        return function(t) { this.textContent = Math.round(interp(t)) }
      })
  }, [data, axes, size, color])
}

// ═══ BUBBLE SCATTER CHART ═══
export function useScatterChart(containerRef, { data, width = 700, height = 320, xKey, yKey, rKey, colorKey, onBubbleClick }) {
  useEffect(() => {
    if (!containerRef.current || !data?.length) return

    const svg = d3.select(containerRef.current)
    svg.selectAll('*').remove()

    const margin = { top: 20, right: 20, bottom: 30, left: 35 }
    const w = width - margin.left - margin.right
    const h = height - margin.top - margin.bottom
    const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

    const xScale = d3.scaleLinear().domain([50, 100]).range([0, w])
    const yScale = d3.scaleLinear().domain([50, 100]).range([h, 0])
    const rScale = d3.scaleLinear().domain(d3.extent(data, d => d[rKey] || 50)).range([6, 22])

    // Grid
    ;[60, 70, 80, 90, 100].forEach(v => {
      g.append('line').attr('x1', xScale(v)).attr('x2', xScale(v)).attr('y1', 0).attr('y2', h)
        .attr('stroke', T.border).attr('stroke-width', 0.5).attr('opacity', 0.3)
      g.append('line').attr('x1', 0).attr('x2', w).attr('y1', yScale(v)).attr('y2', yScale(v))
        .attr('stroke', T.border).attr('stroke-width', 0.5).attr('opacity', 0.3)
    })

    // Bubbles
    const bubbles = g.selectAll('.bubble').data(data).enter()
      .append('g').attr('class', 'bubble').style('cursor', 'pointer')

    bubbles.append('circle')
      .attr('cx', d => xScale(d[xKey]))
      .attr('cy', d => yScale(d[yKey]))
      .attr('r', 0)
      .attr('fill', d => `${tierColors[d[colorKey]] || T.accent}40`)
      .attr('stroke', d => tierColors[d[colorKey]] || T.accent)
      .attr('stroke-width', 1)
      .transition().delay((_, i) => i * 50).duration(600).ease(d3.easeBackOut.overshoot(1.3))
      .attr('r', d => rScale(d[rKey] || 50))

    // Hover
    bubbles.on('mouseenter', function(e, d) {
      d3.select(this).select('circle').transition().duration(150)
        .attr('r', rScale(d[rKey] || 50) + 4).attr('stroke-width', 2.5)
      bubbles.filter(b => b !== d).select('circle').transition().duration(150).attr('opacity', 0.2)
    }).on('mouseleave', function() {
      bubbles.select('circle').transition().duration(150)
        .attr('r', d => rScale(d[rKey] || 50)).attr('stroke-width', 1).attr('opacity', 1)
    }).on('click', (e, d) => onBubbleClick?.(d))

    // Axes
    g.append('g').attr('transform', `translate(0,${h})`).call(d3.axisBottom(xScale).ticks(5))
      .selectAll('text').attr('fill', T.textDim).attr('font-size', 8)
    g.append('g').call(d3.axisLeft(yScale).ticks(5))
      .selectAll('text').attr('fill', T.textDim).attr('font-size', 8)
  }, [data, width, height])
}

// ═══ ARC GAUGE ═══
export function useArcGauge(containerRef, { value, max = 100, size = 90, color, label }) {
  useEffect(() => {
    if (!containerRef.current) return

    const svg = d3.select(containerRef.current)
    svg.selectAll('*').remove()

    const cx = size / 2, cy = size / 2
    const outerR = size / 2 - 4, innerR = outerR - 8
    const startAngle = -Math.PI * 0.75
    const endAngle = Math.PI * 0.75
    const totalAngle = endAngle - startAngle
    const targetAngle = startAngle + (value / max) * totalAngle
    const fillColor = color || T.accent

    const g = svg.append('g').attr('transform', `translate(${cx},${cy})`)

    // Background arc
    const bgArc = d3.arc().innerRadius(innerR).outerRadius(outerR)
      .startAngle(startAngle).endAngle(endAngle).cornerRadius(4)
    g.append('path').attr('d', bgArc()).attr('fill', `${T.border}30`)

    // Value arc (animated)
    const valueArc = d3.arc().innerRadius(innerR).outerRadius(outerR).cornerRadius(4)
    g.append('path')
      .attr('fill', fillColor)
      .transition().duration(1200).ease(d3.easeCubicOut)
      .attrTween('d', () => {
        const interp = d3.interpolate(startAngle, targetAngle)
        return t => valueArc({ startAngle, endAngle: interp(t) })
      })

    // Center score
    const scoreText = g.append('text')
      .attr('text-anchor', 'middle').attr('dominant-baseline', 'middle').attr('y', -4)
      .attr('fill', fillColor).attr('font-size', 18).attr('font-weight', 800).attr('font-family', mono)

    scoreText.transition().duration(1200).ease(d3.easeCubicOut)
      .tween('text', function() {
        const interp = d3.interpolateNumber(0, value)
        return function(t) { this.textContent = Math.round(interp(t)) }
      })

    // Label
    if (label) {
      g.append('text')
        .attr('text-anchor', 'middle').attr('y', 14)
        .attr('fill', T.textDim).attr('font-size', 6).attr('font-family', mono)
        .text(label.slice(0, 12).toUpperCase())
    }
  }, [value, max, size, color, label])
}

// ═══ FUNNEL CHART ═══
export function useFunnelChart(containerRef, { stages, width = 340, height = 220 }) {
  useEffect(() => {
    if (!containerRef.current || !stages?.length) return

    const svg = d3.select(containerRef.current)
    svg.selectAll('*').remove()

    const maxVal = Math.max(...stages.map(s => s.count))
    const stageHeight = height / stages.length - 4
    const g = svg.append('g')

    stages.forEach((stage, i) => {
      const barW = (stage.count / maxVal) * (width * 0.7)
      const nextBarW = i < stages.length - 1 ? (stages[i + 1].count / maxVal) * (width * 0.7) : barW * 0.8
      const x = (width - barW) / 2
      const nextX = (width - nextBarW) / 2
      const y = i * (stageHeight + 4)

      // Trapezoid
      const path = d3.path()
      path.moveTo(x, y)
      path.lineTo(x + barW, y)
      path.lineTo(nextX + nextBarW, y + stageHeight)
      path.lineTo(nextX, y + stageHeight)
      path.closePath()

      g.append('path')
        .attr('d', path.toString())
        .attr('fill', `${stage.color || chartColors[i]}25`)
        .attr('stroke', stage.color || chartColors[i])
        .attr('stroke-width', 0).attr('opacity', 0)
        .transition().delay(i * 120).duration(500)
        .attr('stroke-width', 1.5).attr('opacity', 1)

      // Label
      g.append('text')
        .attr('x', width / 2).attr('y', y + stageHeight / 2)
        .attr('text-anchor', 'middle').attr('dominant-baseline', 'middle')
        .attr('fill', T.text).attr('font-size', 9).attr('font-family', mono).attr('font-weight', 600)
        .text(stage.label)
        .attr('opacity', 0).transition().delay(i * 120 + 200).duration(300).attr('opacity', 1)

      // Count
      g.append('text')
        .attr('x', width - 8).attr('y', y + stageHeight / 2 - 4)
        .attr('text-anchor', 'end').attr('dominant-baseline', 'middle')
        .attr('fill', stage.color || chartColors[i]).attr('font-size', 13).attr('font-family', mono).attr('font-weight', 800)
        .text(stage.count)
    })
  }, [stages, width, height])
}

// ═══ TREEMAP ═══
export function useTreemap(containerRef, { data, width, height, colorScale }) {
  useEffect(() => {
    if (!containerRef.current || !data) return

    const svg = d3.select(containerRef.current)
    svg.selectAll('*').remove()

    const root = d3.hierarchy(data).sum(d => d.value).sort((a, b) => b.value - a.value)
    d3.treemap().size([width, height]).padding(2).round(true)(root)

    const leaves = svg.selectAll('.leaf').data(root.leaves()).enter()
      .append('g').attr('class', 'leaf').attr('transform', d => `translate(${d.x0},${d.y0})`)

    leaves.append('rect')
      .attr('width', d => d.x1 - d.x0).attr('height', d => d.y1 - d.y0)
      .attr('rx', 3).attr('fill', (d, i) => `${chartColors[i % chartColors.length]}30`)
      .attr('stroke', (d, i) => chartColors[i % chartColors.length])
      .attr('stroke-width', 0.5)

    leaves.filter(d => (d.x1 - d.x0) > 40 && (d.y1 - d.y0) > 20)
      .append('text')
      .attr('x', 4).attr('y', 12)
      .attr('fill', T.text).attr('font-size', 8).attr('font-family', mono)
      .text(d => d.data.name?.slice(0, 12))
  }, [data, width, height])
}

// ═══ SPARKLINE ═══
export function useSparkline(containerRef, { data, width = 80, height = 24, color, fill = true }) {
  useEffect(() => {
    if (!containerRef.current || !data?.length) return

    const svg = d3.select(containerRef.current)
    svg.selectAll('*').remove()

    const x = d3.scaleLinear().domain([0, data.length - 1]).range([1, width - 1])
    const y = d3.scaleLinear().domain(d3.extent(data)).range([height - 2, 2])
    const lineColor = color || T.accent

    const line = d3.line().x((_, i) => x(i)).y(d => y(d)).curve(d3.curveCatmullRom)

    if (fill) {
      const area = d3.area().x((_, i) => x(i)).y0(height).y1(d => y(d)).curve(d3.curveCatmullRom)
      svg.append('path').datum(data).attr('d', area).attr('fill', `${lineColor}15`)
    }

    svg.append('path').datum(data).attr('d', line)
      .attr('fill', 'none').attr('stroke', lineColor).attr('stroke-width', 1.5)

    // End dot
    svg.append('circle')
      .attr('cx', x(data.length - 1)).attr('cy', y(data[data.length - 1]))
      .attr('r', 2).attr('fill', lineColor)
  }, [data, width, height, color])
}

export default {
  useForceGraph,
  useRadarChart,
  useScatterChart,
  useArcGauge,
  useFunnelChart,
  useTreemap,
  useSparkline,
}
