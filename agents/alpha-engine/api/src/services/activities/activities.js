import { db } from 'src/lib/db'
import { context } from '@redwoodjs/graphql-server'

export const activities = ({ entityType, limit = 30 }) => {
  const where = entityType ? { entityType } : {}
  return db.activity.findMany({ where, take: limit, orderBy: { createdAt: 'desc' }, include: { user: true } })
}

export const tasks = ({ status }) => {
  const where = { userId: context.currentUser?.id }
  if (status) where.status = status
  return db.task.findMany({ where, orderBy: [{ priority: 'asc' }, { dueDate: 'asc' }] })
}

export const createTask = ({ input }) =>
  db.task.create({ data: { ...input, userId: context.currentUser.id } })

export const updateTaskStatus = ({ id, status }) =>
  db.task.update({ where: { id }, data: { status } })

export const notifications = ({ unreadOnly }) => {
  const where = { userId: context.currentUser?.id }
  if (unreadOnly) where.isRead = false
  return db.notification.findMany({ where, orderBy: { createdAt: 'desc' }, take: 50 })
}

export const markNotificationRead = ({ id }) =>
  db.notification.update({ where: { id }, data: { isRead: true } })
